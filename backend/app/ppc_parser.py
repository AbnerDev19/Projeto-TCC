"""
Extração de um PPC (Projeto Pedagógico de Curso) real, em PDF (seção 28).

PPCs de instituições diferentes têm layouts muito diferentes, então esta
extração é propositalmente heurística e em duas camadas:

  1. Tenta achar a matriz curricular como TABELA (pdfplumber.extract_tables) —
     é o formato mais comum em PPCs bem formatados, geralmente uma tabela por
     período/semestre, com colunas como "Disciplina", "Carga Horária" etc.
  2. Se não encontrar tabelas úteis, cai para um modo por TEXTO: procura
     cabeçalhos de período ("1º período", "2º semestre"...) e, dentro de
     cada bloco, linhas que parecem nome de disciplina.

Por ser heurística, o resultado nunca é aplicado direto no banco — a rota
/api/ppc/analisar apenas devolve uma prévia para o usuário revisar e corrigir
antes de confirmar (/api/ppc/confirmar), então erros de extração são
esperados e o fluxo já foi desenhado para lidar com isso.
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
    r"reconhecimento|autoriza[cç][aã]o|resolu[cç][aã]o|portaria)\s*[:\-]?",
    re.IGNORECASE,
)

REGEX_PERIODO = re.compile(
    r"(\d{1,2})\s*[ºo°]?\s*[-–]?\s*(per[íi]odo|semestre)", re.IGNORECASE
)

REGEX_CH = re.compile(r"(\d{2,4})\s*(?:h\b|horas?|h/a|hs)", re.IGNORECASE)


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
            idx_ch = next((i for i, c in enumerate(cabecalho) if "carga" in c or c == "ch"), None)
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
                if idx_ch is not None and idx_ch < len(linha) and linha[idx_ch]:
                    ch_match = REGEX_CH.search(str(linha[idx_ch])) or re.search(r"\d{2,4}", str(linha[idx_ch]))
                    if ch_match:
                        ch = int(re.sub(r"\D", "", ch_match.group(0))[:4] or 0) or None

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
    semestre + avisos sobre a qualidade da extração.
    """
    texto_paginas, tabelas_paginas = extrair_texto_e_tabelas(pdf_bytes)

    disciplinas = _extrair_via_tabelas(texto_paginas, tabelas_paginas)
    metodo = "tabela"
    if len(disciplinas) < 3:
        disciplinas = _extrair_via_texto(texto_paginas)
        metodo = "texto"

    disciplinas = _deduplicar(disciplinas)
    disciplinas.sort(key=lambda d: (d["semestre"], d["nome"]))

    metadados = _extrair_metadados_curso(texto_paginas)

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
    if not metadados["nome_curso"]:
        avisos.append("Não foi possível identificar o nome do curso automaticamente — preencha manualmente.")

    return {
        "metodo_extracao": metodo,
        "avisos": avisos,
        "curso_sugerido": metadados,
        "disciplinas": disciplinas,
    }
