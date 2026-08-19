"""
Extração de um PPC (Projeto Pedagógico de Curso) real, em PDF (seção 28).

PPCs de instituições diferentes têm layouts muito diferentes, então esta
extração é propositalmente heurística e em camadas:

  1. Tenta achar a matriz curricular como TABELA (pdfplumber.extract_tables) —
     o formato mais comum em PPCs bem formatados, geralmente uma tabela por
     período/semestre, com colunas como "Disciplina", "Carga Horária" etc.
     Lida também com carga horária dividida em colunas "Teórica"/"Prática".
  2. Se não encontrar tabelas úteis, cai para um modo por TEXTO: procura
     cabeçalhos de período ("1º período", "2º semestre"...) e, dentro de
     cada bloco, linhas que parecem nome de disciplina.
  3. Depois de ter a lista de disciplinas, tenta casar cada uma com um
     ementário (seção "EMENTAS"/"EMENTÁRIO", comum em PPCs brasileiros) para
     trazer uma descrição real do que a disciplina ensina — não só o nome.

Cada disciplina extraída recebe um sinal de "confianca": False quando o
método de extração é menos confiável (fallback por texto) ou quando a carga
horária não foi encontrada, para que a tela de revisão possa destacar os
itens que merecem mais atenção do usuário antes de confirmar.

Por ser heurística, o resultado nunca é aplicado direto no banco — a rota
/api/ppc/analisar apenas devolve uma prévia para o usuário revisar e corrigir
antes de confirmar (/api/ppc/confirmar).
"""
import io
import re
import unicodedata

import pdfplumber

PALAVRAS_CABECALHO_TABELA = {
    "disciplina", "componente curricular", "unidade curricular", "componente",
    "carga horaria", "ch", "periodo", "semestre", "codigo",
}

# linhas que quase certamente NÃO são disciplinas (ruído comum de PPCs:
# cabeçalhos, metadados do curso, rodapés etc.)
LINHAS_IGNORAR = re.compile(
    r"^(p[aá]gina|sum[aá]rio|anexo|refer[eê]ncias?|total|carga\s*hor[aá]ria\s*total|"
    r"observa[cç][oõ]es?|coordena[cç][aã]o|projeto\s+pedag[oó]gico|curso\s+de\s+gradua[cç][aã]o|"
    r"institui[cç][aã]o|modalidade|carga\s*hor[aá]ria(?!\s+\w)|dura[cç][aã]o|"
    r"reconhecimento|autoriza[cç][aã]o|resolu[cç][aã]o|portaria|ementa)\s*[:\-]?",
    re.IGNORECASE,
)

REGEX_PERIODO = re.compile(
    r"(\d{1,2})\s*[ºo°]?\s*[-–]?\s*(per[íi]odo|semestre)", re.IGNORECASE
)

REGEX_CH = re.compile(r"(\d{2,4})\s*(?:h\b|horas?|h/a|hs)", re.IGNORECASE)

REGEX_EMENTARIO_TITULO = re.compile(
    r"ement[aá]rio|ementas?\s+(das|dos)\s+(disciplinas|componentes)", re.IGNORECASE
)

TAMANHO_MAX_EMENTA = 700


def _normalizar(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.lower().strip()


def _linha_parece_disciplina(linha: str) -> bool:
    linha = linha.strip()
    if len(linha) < 4 or len(linha) > 120:
        return False
    if LINHAS_IGNORAR.match(linha):
        return False
    if re.fullmatch(r"[\d\s./ºo°-]+", linha):
        return False
    letras = sum(c.isalpha() for c in linha)
    if letras < 4:
        return False
    return True


def _limpar_nome_disciplina(linha: str) -> str:
    # remove código de disciplina no início (ex: "COMP101 - Algoritmos")
    linha = re.sub(r"^[A-Z]{2,6}\d{2,4}\s*[-–:]\s*", "", linha)
    # remove carga horária colada no fim (ex: "Algoritmos 80h")
    linha = REGEX_CH.sub("", linha)
    linha = re.sub(r"\s{2,}", " ", linha).strip(" -–:\t")
    return linha


def extrair_texto_e_tabelas(pdf_bytes: bytes):
    texto_paginas = []
    tabelas_paginas = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            texto_paginas.append(page.extract_text() or "")
            try:
                tabelas_paginas.append(page.extract_tables() or [])
            except Exception:
                tabelas_paginas.append([])
    return texto_paginas, tabelas_paginas


def _extrair_ch_de_celula(valor) -> int | None:
    if not valor:
        return None
    texto = str(valor)
    m = REGEX_CH.search(texto) or re.search(r"\d{2,4}", texto)
    if not m:
        return None
    digitos = re.sub(r"\D", "", m.group(0))[:4]
    return int(digitos) if digitos else None


def _dividir_curriculo_e_ementario(texto_paginas: list[str]) -> tuple[list[str], str]:
    """
    Separa o texto do documento em duas partes: a matriz curricular (antes
    do ementário) e o texto do ementário em si. Isso evita que a extração
    de disciplinas "vaze" para dentro do ementário — as descrições de
    conteúdo programático têm o formato de texto corrido e, sem essa
    separação, seriam capturadas incorretamente como se fossem disciplinas.

    Mantém a mesma quantidade de páginas em `texto_paginas` (só esvazia o
    texto após o ementário) para preservar o alinhamento com `tabelas_paginas`.
    """
    resultado_curriculo = list(texto_paginas)
    partes_ementario: list[str] = []
    encontrado = False

    for i, pagina in enumerate(texto_paginas):
        if encontrado:
            partes_ementario.append(pagina)
            resultado_curriculo[i] = ""
            continue
        m = REGEX_EMENTARIO_TITULO.search(pagina)
        if m:
            resultado_curriculo[i] = pagina[:m.start()]
            partes_ementario.append(pagina[m.start():])
            encontrado = True

    return resultado_curriculo, "\n".join(partes_ementario)


def _extrair_via_tabelas(texto_paginas, tabelas_paginas):
    """Camada 1: tenta ler a matriz curricular a partir de tabelas do PDF."""
    disciplinas = []
    periodo_atual = 1

    for pagina_idx, tabelas in enumerate(tabelas_paginas):
        texto_pagina_norm = _normalizar(texto_paginas[pagina_idx])
        m = REGEX_PERIODO.search(texto_pagina_norm)
        if m:
            periodo_atual = int(m.group(1))

        for tabela in tabelas:
            if not tabela or len(tabela) < 2:
                continue

            cabecalho = [_normalizar(c or "") for c in tabela[0]]
            cabecalho_valido = any(
                any(p in c for p in PALAVRAS_CABECALHO_TABELA) for c in cabecalho
            )
            if not cabecalho_valido:
                continue

            idx_nome = next(
                (i for i, c in enumerate(cabecalho)
                 if "disciplina" in c or "componente" in c or "unidade curricular" in c),
                None,
            )
            # carga horária pode vir em uma única coluna, ou dividida em
            # teórica/prática — nesse caso somamos as duas.
            idx_ch = next(
                (i for i, c in enumerate(cabecalho)
                 if ("carga" in c or c == "ch") and "teoric" not in c and "pratic" not in c),
                None,
            )
            idx_ch_teorica = next((i for i, c in enumerate(cabecalho) if "teoric" in c), None)
            idx_ch_pratica = next((i for i, c in enumerate(cabecalho) if "pratic" in c), None)
            idx_periodo = next(
                (i for i, c in enumerate(cabecalho) if "periodo" in c or "semestre" in c), None
            )
            if idx_nome is None:
                continue

            for linha in tabela[1:]:
                if not linha or idx_nome >= len(linha):
                    continue
                nome_bruto = (linha[idx_nome] or "").replace("\n", " ").strip()
                if not _linha_parece_disciplina(nome_bruto):
                    continue

                ch = None
                if idx_ch is not None and idx_ch < len(linha):
                    ch = _extrair_ch_de_celula(linha[idx_ch])
                elif idx_ch_teorica is not None or idx_ch_pratica is not None:
                    ch_t = _extrair_ch_de_celula(linha[idx_ch_teorica]) if idx_ch_teorica is not None and idx_ch_teorica < len(linha) else None
                    ch_p = _extrair_ch_de_celula(linha[idx_ch_pratica]) if idx_ch_pratica is not None and idx_ch_pratica < len(linha) else None
                    if ch_t or ch_p:
                        ch = (ch_t or 0) + (ch_p or 0)

                periodo = periodo_atual
                if idx_periodo is not None and idx_periodo < len(linha) and linha[idx_periodo]:
                    p_match = re.search(r"\d{1,2}", str(linha[idx_periodo]))
                    if p_match:
                        periodo = int(p_match.group(0))

                disciplinas.append({
                    "nome": _limpar_nome_disciplina(nome_bruto),
                    "semestre": max(1, min(periodo, 20)),
                    "carga_horaria": ch,
                    "ementa": "",
                    "confianca": ch is not None,
                })

    return disciplinas


def _extrair_via_texto(texto_paginas):
    """Camada 2 (fallback): heurística puramente textual, por blocos de período."""
    texto_completo = "\n".join(texto_paginas)
    linhas = [l for l in texto_completo.split("\n") if l.strip()]

    disciplinas = []
    periodo_atual = 1
    for linha in linhas:
        m = REGEX_PERIODO.search(_normalizar(linha))
        if m and len(linha.strip()) < 40:
            periodo_atual = int(m.group(1))
            continue

        if not _linha_parece_disciplina(linha):
            continue

        nome = _limpar_nome_disciplina(linha)
        if not nome:
            continue

        ch_match = REGEX_CH.search(linha)
        ch = int(ch_match.group(1)) if ch_match else None

        disciplinas.append({
            "nome": nome,
            "semestre": periodo_atual,
            "carga_horaria": ch,
            "ementa": "",
            # extração por texto é sempre marcada como menos confiável,
            # mesmo quando acha a carga horária — pede revisão do usuário.
            "confianca": False,
        })

    return disciplinas


def _deduplicar(disciplinas: list[dict]) -> list[dict]:
    vistos = set()
    resultado = []
    for d in disciplinas:
        chave = (_normalizar(d["nome"]), d["semestre"])
        if chave in vistos or not d["nome"]:
            continue
        vistos.add(chave)
        resultado.append(d)
    return resultado


def _associar_ementario(disciplinas: list[dict], texto_ementario: str) -> None:
    """
    Camada 3: a partir do texto do ementário (já separado da matriz
    curricular por `_dividir_curriculo_e_ementario`), preenche o campo
    'ementa' de cada disciplina já extraída, casando pelo nome. Modifica a
    lista `disciplinas` in-place; não falha se não achar nada.
    """
    if not texto_ementario:
        return

    m = REGEX_EMENTARIO_TITULO.search(texto_ementario)
    texto_apos_titulo = texto_ementario[m.end():] if m else texto_ementario
    linhas = [l.strip() for l in texto_apos_titulo.split("\n") if l.strip()]

    # nome normalizado -> disciplina (para casar heading de ementa por nome)
    por_nome = {_normalizar(d["nome"]): d for d in disciplinas}
    if not por_nome:
        return

    disciplina_atual = None
    buffer: list[str] = []

    def _fechar_bloco():
        if disciplina_atual is not None and buffer:
            texto = " ".join(buffer).strip()
            if len(texto) > 15:  # ignora blocos vazios/ruído
                disciplina_atual["ementa"] = texto[:TAMANHO_MAX_EMENTA]

    for linha in linhas:
        linha_norm = _normalizar(_limpar_nome_disciplina(linha))
        candidato = por_nome.get(linha_norm)
        if candidato is not None:
            _fechar_bloco()
            disciplina_atual = candidato
            buffer = []
            continue
        if disciplina_atual is not None:
            if LINHAS_IGNORAR.match(linha):
                continue
            buffer.append(linha)
            if len(" ".join(buffer)) > TAMANHO_MAX_EMENTA:
                _fechar_bloco()
                disciplina_atual = None
                buffer = []

    _fechar_bloco()


def _extrair_metadados_curso(texto_paginas: list[str]) -> dict:
    texto = "\n".join(texto_paginas[:3])  # metadados normalmente ficam nas primeiras páginas

    nome_curso = None
    m = re.search(
        r"curso\s+(?:de\s+)?(?:graduação\s+em|bacharelado\s+em|tecnologia\s+em|licenciatura\s+em)\s+([^\n.]{3,80})",
        texto, re.IGNORECASE,
    )
    if m:
        nome_curso = m.group(0).strip(" .:-")

    instituicao = None
    m = re.search(r"institui[cç][ãa]o\s*[:\-]\s*([^\n]{3,100})", texto, re.IGNORECASE)
    if m:
        instituicao = m.group(1).strip(" .:-")

    ch_total = None
    m = re.search(r"carga\s*hor[áa]ria\s*total\s*[:\-]?\s*(\d{3,5})", texto, re.IGNORECASE)
    if m:
        ch_total = int(m.group(1))

    modalidade = None
    texto_norm = _normalizar(texto)
    if "ead" in texto_norm or "ensino a distancia" in texto_norm or "educacao a distancia" in texto_norm:
        modalidade = "EAD"
    elif "hibrid" in texto_norm:
        modalidade = "Híbrido"
    elif "presencial" in texto_norm:
        modalidade = "Presencial"

    return {
        "nome_curso": nome_curso,
        "instituicao": instituicao,
        "carga_horaria_total": ch_total,
        "modalidade": modalidade,
    }


def analisar_ppc(pdf_bytes: bytes) -> dict:
    """
    Função principal: recebe os bytes de um PDF de PPC e devolve uma prévia
    (não persistida) com metadados do curso + disciplinas extraídas por
    semestre (com ementa, quando encontrada, e um sinal de confiança) +
    avisos sobre a qualidade da extração.
    """
    texto_paginas, tabelas_paginas = extrair_texto_e_tabelas(pdf_bytes)
    texto_paginas_curriculo, texto_ementario = _dividir_curriculo_e_ementario(texto_paginas)

    disciplinas = _extrair_via_tabelas(texto_paginas_curriculo, tabelas_paginas)
    metodo = "tabela"
    if len(disciplinas) < 3:
        disciplinas = _extrair_via_texto(texto_paginas_curriculo)
        metodo = "texto"

    disciplinas = _deduplicar(disciplinas)
    disciplinas.sort(key=lambda d: (d["semestre"], d["nome"]))

    _associar_ementario(disciplinas, texto_ementario)

    metadados = _extrair_metadados_curso(texto_paginas)

    com_ementa = sum(1 for d in disciplinas if d["ementa"])
    baixa_confianca = sum(1 for d in disciplinas if not d["confianca"])

    avisos = []
    if not disciplinas:
        avisos.append(
            "Não foi possível identificar disciplinas automaticamente neste PDF. "
            "Isso pode acontecer com PPCs escaneados como imagem, sem texto selecionável. "
            "Adicione as disciplinas manualmente na revisão abaixo."
        )
    elif metodo == "texto":
        avisos.append(
            "Não foi encontrada uma tabela de matriz curricular clara — a extração usou "
            "o texto corrido do documento e pode conter itens incorretos. Revise a lista "
            "com atenção antes de confirmar."
        )
    elif baixa_confianca:
        avisos.append(
            f"{baixa_confianca} disciplina(s) foram identificadas mas sem carga horária "
            "clara — vale conferir esses itens antes de confirmar."
        )
    if not metadados["nome_curso"]:
        avisos.append("Não foi possível identificar o nome do curso automaticamente — preencha manualmente.")
    if disciplinas and not com_ementa:
        avisos.append(
            "Não foi encontrado um ementário no documento — as disciplinas foram "
            "extraídas só pelo nome, sem descrição do conteúdo."
        )

    return {
        "metodo_extracao": metodo,
        "avisos": avisos,
        "curso_sugerido": metadados,
        "disciplinas": disciplinas,
    }
