"""
Busca ao vivo de formações "reais" (seção do pedido do usuário: cursos que a
pessoa pode realmente fazer, onde, e período de inscrição).

Diferente do restante do sistema (que é 100% baseado em dados cadastrados
no banco), esta busca acontece em tempo real, a cada chamada, direto na web —
por isso é mais lenta e mais frágil do que o resto da API: depende de sites
de terceiros estarem no ar e responderem dentro do timeout.

Não usamos nenhuma API paga (Google/Bing Custom Search exigem chave e
faturamento): a busca é feita via a versão HTML "lite" do DuckDuckGo, que não
exige chave de API. É uma solução propositalmente simples — se o projeto for
para produção séria, trocar por uma API de busca paga (Serper, Tavily, Bing)
tornaria isso mais estável; o código já isola essa lógica em `_buscar()` para
facilitar a troca.

Por ser busca ao vivo em texto livre, o "período de inscrição" nem sempre é
encontrado — quando não é, o card deixa isso explícito e aponta para a fonte
oficial, em vez de inventar uma data.
"""
import re
import unicodedata
import httpx
from bs4 import BeautifulSoup

TIMEOUT = httpx.Timeout(8.0, connect=5.0)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TrilhaAcademica/1.0; +https://example.org)"
}

REGEX_INSCRICAO = re.compile(
    r"(inscri[cç][õoã]es?[^.]{0,80}(?:at[ée]|de|entre)[^.]{0,60}\d{1,2}[^.]{0,40}\d{4}?|"
    r"vestibular[^.]{0,60}\d{4}|processo\s+seletivo[^.]{0,80})",
    re.IGNORECASE,
)
REGEX_MODALIDADE = re.compile(r"\b(EAD|ead|presencial|h[íi]brido|online)\b")


def _normalizar(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def _buscar(query: str, max_resultados: int = 5) -> list[dict]:
    """Busca no DuckDuckGo HTML (sem necessidade de chave de API) e devolve [{titulo, url, resumo}]."""
    resultados = []
    try:
        with httpx.Client(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True) as client:
            resp = client.post("https://html.duckduckgo.com/html/", data={"q": query})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.select(".result")[:max_resultados]:
                link_tag = item.select_one(".result__a")
                snippet_tag = item.select_one(".result__snippet")
                if not link_tag:
                    continue
                url = link_tag.get("href", "")
                titulo = link_tag.get_text(strip=True)
                resumo = snippet_tag.get_text(strip=True) if snippet_tag else ""
                if url and titulo:
                    resultados.append({"titulo": titulo, "url": url, "resumo": resumo})
    except (httpx.HTTPError, httpx.TimeoutException):
        return []
    return resultados


def _extrair_instituicao(titulo: str) -> str:
    # heurística simples: parte do título antes de " - " ou " | " costuma ser a instituição/site
    for sep in [" - ", " | ", " – "]:
        if sep in titulo:
            partes = titulo.split(sep)
            return partes[-1].strip() if len(partes[-1]) < 40 else partes[0].strip()
    return titulo[:60]


def _montar_card(resultado: dict, tipo: str) -> dict:
    texto = f"{resultado['titulo']} {resultado['resumo']}"

    periodo_match = REGEX_INSCRICAO.search(texto)
    periodo = periodo_match.group(0).strip().capitalize() if periodo_match else None

    modalidade_match = REGEX_MODALIDADE.search(texto)
    modalidade = modalidade_match.group(0).upper() if modalidade_match else None

    return {
        "tipo": tipo,
        "titulo": resultado["titulo"],
        "instituicao_provavel": _extrair_instituicao(resultado["titulo"]),
        "modalidade": modalidade,
        "periodo_inscricao": periodo,
        "resumo": resultado["resumo"],
        "fonte_url": resultado["url"],
    }


def buscar_formacoes_reais(area_nome: str, estado: str | None = None) -> dict:
    """
    Faz 3 buscas ao vivo (graduação, curso livre/complementar, pós-graduação)
    relacionadas à área de interesse e devolve resultados estruturados,
    cada um citando a fonte para o usuário conferir os detalhes oficiais.
    """
    local = f" {estado}" if estado else " Brasil"

    queries = {
        "graduacao": f'graduação "{area_nome}" inscrições{local}',
        "curso_livre": f'curso livre online "{area_nome}" certificado inscrições',
        "pos_graduacao": f'pós-graduação especialização "{area_nome}" inscrições{local}',
    }

    resultado = {"area": area_nome, "estado": estado, "formacoes": [], "erro": None}

    total_encontrado = 0
    for tipo, query in queries.items():
        brutos = _buscar(query, max_resultados=4)
        for r in brutos:
            resultado["formacoes"].append(_montar_card(r, tipo))
        total_encontrado += len(brutos)

    if total_encontrado == 0:
        resultado["erro"] = (
            "Não foi possível buscar formações agora (a busca ao vivo pode estar "
            "temporariamente indisponível). Tente novamente em instantes."
        )

    return resultado
