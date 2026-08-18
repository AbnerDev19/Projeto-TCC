"""
Motor de recomendação — versão 1 (baseada em conteúdo / pontuação).

Não usa Machine Learning (de propósito — seção 30 do planejamento).
A ideia:
  1. Cada disciplina do curso do estudante está ligada a 0..N áreas,
     cada ligação tem um "peso" (o quanto aquela disciplina contribui
     para a área — ex: Banco de Dados pesa mais para "Banco de Dados"
     do que "Matemática" pesa para "Ciência de Dados").
  2. Somamos os pesos das disciplinas do estudante para a área de
     interesse escolhida e comparamos com o peso "ideal" da área
     (soma de todos os pesos possíveis cadastrados para aquela área).
  3. compatibilidade% = pontos_do_estudante / pontos_maximos_da_area

Isso corresponde exatamente ao exemplo do documento:
  Banco de Dados = 3, Programação = 3, Estatística = 2, Matemática = 2,
  IA = 3  ->  Compatibilidade = 82%
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


def calcular_compatibilidade(db: Session, curso_id: int, area_id: int):
    """Retorna (percentual, lista_disciplinas_relacionadas_cursadas)."""

    # Pontos "ideais" da área = nível de domínio esperado, cadastrado na
    # própria área (não depende de quais disciplinas um curso específico
    # oferece — do contrário, um curso pequeno sempre bateria 100%).
    area = db.query(models.Area).filter(models.Area.id == area_id).first()
    pontos_maximos = (area.pontos_ideais if area else 0) or 0

    if pontos_maximos == 0:
        return 0.0, []

    # Disciplinas do curso do estudante que contribuem para essa área
    resultados = (
        db.query(models.Disciplina.nome, models.disciplina_area.c.peso)
        .join(models.disciplina_area, models.Disciplina.id == models.disciplina_area.c.disciplina_id)
        .filter(
            models.Disciplina.curso_id == curso_id,
            models.disciplina_area.c.area_id == area_id,
        )
        .all()
    )

    pontos_estudante = sum(peso for _, peso in resultados)
    disciplinas_relacionadas = [nome for nome, _ in resultados]

    percentual = min(100.0, round((pontos_estudante / pontos_maximos) * 100, 1))
    return percentual, disciplinas_relacionadas


def gerar_justificativa(area_nome: str, disciplinas: list, percentual: float) -> str:
    if not disciplinas:
        return (
            f"Sua grade curricular ainda não possui disciplinas fortemente "
            f"relacionadas a {area_nome}. Essa trilha exigirá mais estudo "
            f"complementar por fora do curso."
        )
    lista = ", ".join(disciplinas)
    return (
        f"Sua formação possui {len(disciplinas)} disciplina(s) relacionada(s) a "
        f"{area_nome} ({lista}), o que resulta em {percentual}% de compatibilidade. "
        f"Isso indica uma base {'sólida' if percentual >= 60 else 'inicial'} para seguir essa trilha."
    )


def analisar_lacunas(db: Session, curso_id: int, area_id: int):
    """Compara disciplinas já cursadas com o que falta para a área (seção 15 - Gap Analysis)."""
    _, cursadas = calcular_compatibilidade(db, curso_id, area_id)
    cursadas_set = set(cursadas)

    todas_da_area = (
        db.query(models.Disciplina.nome)
        .join(models.disciplina_area, models.Disciplina.id == models.disciplina_area.c.disciplina_id)
        .filter(models.disciplina_area.c.area_id == area_id)
        .distinct()
        .all()
    )
    todas_da_area = {nome for (nome,) in todas_da_area}

    faltando = list(todas_da_area - cursadas_set)
    return list(cursadas_set), faltando
