"""
Modelos do banco de dados — Trilha Acadêmica
Baseado no esquema descrito na seção 24 do planejamento do TCC.
"""
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Table, ARRAY
)
from sqlalchemy.orm import relationship
from .database import Base

# Tabela associativa N:N — disciplina <-> área (seção 25)
disciplina_area = Table(
    "disciplina_area",
    Base.metadata,
    Column("disciplina_id", Integer, ForeignKey("disciplinas.id"), primary_key=True),
    Column("area_id", Integer, ForeignKey("areas.id"), primary_key=True),
    Column("peso", Integer, default=1),  # força da relação disciplina->área (usado no motor de recomendação)
)


class Instituicao(Base):
    __tablename__ = "instituicoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String)
    estado = Column(String)

    cursos = relationship("Curso", back_populates="instituicao")


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    instituicao_id = Column(Integer, ForeignKey("instituicoes.id"))
    carga_horaria = Column(Integer)
    duracao_semestres = Column(Integer)
    modalidade = Column(String)
    # "ppc_upload" (extraído automaticamente de um PDF real) ou "demonstracao"
    origem = Column(String, default="demonstracao")

    instituicao = relationship("Instituicao", back_populates="cursos")
    disciplinas = relationship("Disciplina", back_populates="curso")


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    carga_horaria = Column(Integer)
    ementa = Column(Text)
    curso_id = Column(Integer, ForeignKey("cursos.id"))

    curso = relationship("Curso", back_populates="disciplinas")
    areas = relationship("Area", secondary=disciplina_area, back_populates="disciplinas")


class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(Text)
    # Pontuação "ideal" (domínio completo) usada como denominador no cálculo
    # de compatibilidade — representa o quanto de conhecimento a área exige,
    # independente do que qualquer curso específico oferece (seção 30-31).
    pontos_ideais = Column(Integer, default=10)

    disciplinas = relationship("Disciplina", secondary=disciplina_area, back_populates="areas")
    etapas_trilha = relationship("EtapaTrilha", back_populates="area")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    objetivo = Column(String)  # trabalhar / especializacao / mestrado / pesquisa / concurso / ainda_nao_sei
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=True)

    interesses = relationship("InteresseUsuario", back_populates="usuario")


class InteresseUsuario(Base):
    __tablename__ = "interesses_usuario"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    area_id = Column(Integer, ForeignKey("areas.id"), primary_key=True)

    usuario = relationship("Usuario", back_populates="interesses")
    area = relationship("Area")


class CursoComplementar(Base):
    __tablename__ = "cursos_complementares"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    instituicao = Column(String)
    modalidade = Column(String)
    carga_horaria = Column(Integer)
    area_id = Column(Integer, ForeignKey("areas.id"))
    link = Column(String)

    area = relationship("Area")


class PosGraduacao(Base):
    __tablename__ = "pos_graduacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String)  # especializacao / mestrado / doutorado
    instituicao = Column(String)
    area_id = Column(Integer, ForeignKey("areas.id"))
    modalidade = Column(String)

    area = relationship("Area")


class Trilha(Base):
    __tablename__ = "trilhas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id"))

    area = relationship("Area")
    etapas = relationship("EtapaTrilha", back_populates="trilha", order_by="EtapaTrilha.ordem")


class EtapaTrilha(Base):
    __tablename__ = "etapas_trilha"

    id = Column(Integer, primary_key=True, index=True)
    trilha_id = Column(Integer, ForeignKey("trilhas.id"))
    ordem = Column(Integer, nullable=False)
    conhecimento = Column(String, nullable=False)
    curso_sugerido = Column(String)
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=True)

    trilha = relationship("Trilha", back_populates="etapas")
    area = relationship("Area")
