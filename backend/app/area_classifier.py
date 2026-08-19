"""
Classificador automático de disciplina -> área de conhecimento.

Antes, a relação disciplina-área era 100% manual (DISCIPLINA_AREA em
seed.py), o que só funcionava para o curso de exemplo. Agora que o PPC
real é extraído de um PDF enviado pelo usuário (seção 28), não existe
curadoria manual possível: cada disciplina extraída precisa ser
classificada automaticamente, na hora, contra as áreas conhecidas.

A abordagem é deliberadamente simples e auditável (nada de modelo externo
ou chamada de API paga): contagem de palavras-chave por área, comparando
o nome da disciplina (peso maior) e a ementa (peso menor), com o texto
normalizado (sem acento, minúsculo) para tolerar variações de digitação
comuns em PDFs de PPC.
"""
import unicodedata
from typing import Iterable, List, Tuple

from .area_data import AREA_DEFINICOES


def _normalizar(texto: str) -> str:
    """Remove acentos e baixa a caixa, para comparação tolerante."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.lower()


def classificar_disciplina(nome: str, ementa: str = "") -> List[Tuple[str, int]]:
    """
    Retorna uma lista [(nome_da_area, peso)] para a disciplina informada.

    peso vai de 1 a 3 (mesma escala usada no restante do sistema para
    disciplina_area). Uma disciplina pode pertencer a mais de uma área
    (ex: "Banco de Dados para Aprendizado de Máquina" toca Banco de Dados
    e Inteligência Artificial). Áreas sem nenhuma palavra-chave encontrada
    não entram no resultado.
    """
    nome_norm = _normalizar(nome)
    ementa_norm = _normalizar(ementa)

    resultados: List[Tuple[str, int]] = []

    for area_nome, definicao in AREA_DEFINICOES.items():
        pontuacao = 0
        for termo in definicao["keywords"]:
            termo_norm = _normalizar(termo)
            if termo_norm in nome_norm:
                pontuacao += 3  # bate no título da disciplina: sinal forte
            elif termo_norm in ementa_norm:
                pontuacao += 1  # bate só na ementa: sinal fraco

        if pontuacao <= 0:
            continue

        # Converte a pontuação bruta em peso 1-3 (mesma escala do resto do app)
        if pontuacao >= 5:
            peso = 3
        elif pontuacao >= 3:
            peso = 2
        else:
            peso = 1

        resultados.append((area_nome, peso))

    resultados.sort(key=lambda item: item[1], reverse=True)
    return resultados


def area_mais_provavel(nome: str, ementa: str = "") -> str | None:
    """Atalho: devolve só o nome da área com maior peso, se houver alguma."""
    resultado = classificar_disciplina(nome, ementa)
    return resultado[0][0] if resultado else None


def areas_relevantes_para_curso(disciplinas: Iterable[dict]) -> set[str]:
    """
    Dado um conjunto de disciplinas extraídas (dicts com 'nome' e 'ementa'),
    devolve o conjunto de áreas que fazem sentido oferecer como opção de
    interesse para esse curso — evita listar as ~19 áreas do sistema quando
    só um punhado delas tem relação real com a grade extraída do PPC.
    """
    relevantes: set[str] = set()
    for d in disciplinas:
        for area_nome, _peso in classificar_disciplina(d.get("nome", ""), d.get("ementa", "") or ""):
            relevantes.add(area_nome)
    return relevantes
