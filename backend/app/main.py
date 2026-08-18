from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os

from . import models, schemas, recommendation, seed
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)
seed.seed()  # popula o banco na primeira execução; não faz nada se já houver dados

app = FastAPI(
    title="Trilha Acadêmica API",
    description="Sistema de recomendação de percursos de formação acadêmica a partir da análise de PPCs.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção: restringir ao domínio do front-end
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


@app.get("/api/cursos", response_model=List[schemas.CursoOut], tags=["Cursos"])
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(models.Curso).all()


@app.get("/api/cursos/{curso_id}/disciplinas", response_model=List[schemas.DisciplinaOut], tags=["Cursos"])
def listar_disciplinas(curso_id: int, db: Session = Depends(get_db)):
    disciplinas = db.query(models.Disciplina).filter(models.Disciplina.curso_id == curso_id).order_by(models.Disciplina.semestre).all()
    if not disciplinas:
        raise HTTPException(status_code=404, detail="Curso não encontrado ou sem disciplinas cadastradas.")
    return disciplinas


@app.get("/api/areas", response_model=List[schemas.AreaOut], tags=["Áreas"])
def listar_areas(db: Session = Depends(get_db)):
    return db.query(models.Area).all()


@app.get(
    "/api/cursos/{curso_id}/recomendacao/{area_id}",
    response_model=schemas.RecomendacaoOut,
    tags=["Recomendação"],
)
def recomendar_trilha(curso_id: int, area_id: int, db: Session = Depends(get_db)):
    """
    Motor de recomendação (seções 14, 15, 30-31 do documento):
    dado um curso e uma área de interesse, calcula compatibilidade,
    disciplinas relacionadas já cursadas, trilha sugerida, cursos
    complementares e pós-graduações compatíveis.
    """
    area = db.query(models.Area).filter(models.Area.id == area_id).first()
    curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if not area or not curso:
        raise HTTPException(status_code=404, detail="Curso ou área não encontrados.")

    percentual, disciplinas_relacionadas = recommendation.calcular_compatibilidade(db, curso_id, area_id)
    justificativa = recommendation.gerar_justificativa(area.nome, disciplinas_relacionadas, percentual)

    trilha = db.query(models.Trilha).filter(models.Trilha.area_id == area_id).first()
    etapas = trilha.etapas if trilha else []

    cursos_complementares = db.query(models.CursoComplementar).filter(models.CursoComplementar.area_id == area_id).all()
    pos_graduacoes = db.query(models.PosGraduacao).filter(models.PosGraduacao.area_id == area_id).all()

    return schemas.RecomendacaoOut(
        area=area,
        compatibilidade_percentual=percentual,
        disciplinas_relacionadas_cursadas=disciplinas_relacionadas,
        trilha_sugerida=etapas,
        cursos_complementares=cursos_complementares,
        pos_graduacoes=pos_graduacoes,
        justificativa=justificativa,
    )


@app.get("/api/cursos/{curso_id}/gap/{area_id}", tags=["Recomendação"])
def analisar_lacunas(curso_id: int, area_id: int, db: Session = Depends(get_db)):
    """Gap analysis (seção 15): o que já foi cursado x o que falta para a área."""
    cursadas, faltando = recommendation.analisar_lacunas(db, curso_id, area_id)
    return {"disciplinas_ja_cursadas": cursadas, "disciplinas_recomendadas": faltando}


@app.get("/api/cursos/{curso_id}/dashboard", tags=["Dashboard"])
def dashboard(curso_id: int, db: Session = Depends(get_db)):
    """
    Retorna, para todas as áreas, o percentual de compatibilidade do curso —
    usado para montar a tela de dashboard (seção 33 do documento).
    """
    areas = db.query(models.Area).all()
    resultado = []
    for area in areas:
        percentual, _ = recommendation.calcular_compatibilidade(db, curso_id, area.id)
        resultado.append({"area": area.nome, "compatibilidade_percentual": percentual})
    resultado.sort(key=lambda x: x["compatibilidade_percentual"], reverse=True)
    return resultado


@app.post("/api/usuarios", response_model=schemas.UsuarioOut, tags=["Usuários"])
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    # Nota: em produção, usar bcrypt/passlib para o hash da senha (RNF02 do documento)
    novo = models.Usuario(
        nome=usuario.nome, email=usuario.email, senha_hash=f"hash:{usuario.senha}",
        objetivo=usuario.objetivo, curso_id=usuario.curso_id,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# Serve o front-end básico (arquivos estáticos) na raiz, se a pasta existir
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
