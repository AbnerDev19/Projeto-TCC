from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class AreaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: Optional[str] = None


class DisciplinaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    semestre: int
    carga_horaria: Optional[int] = None
    ementa: Optional[str] = None
    areas: List[AreaOut] = []


class CursoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    carga_horaria: Optional[int] = None
    duracao_semestres: Optional[int] = None
    modalidade: Optional[str] = None


class CursoComplementarOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    instituicao: Optional[str] = None
    modalidade: Optional[str] = None
    carga_horaria: Optional[int] = None
    link: Optional[str] = None


class PosGraduacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    tipo: Optional[str] = None
    instituicao: Optional[str] = None
    modalidade: Optional[str] = None


class EtapaTrilhaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ordem: int
    conhecimento: str
    curso_sugerido: Optional[str] = None


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    objetivo: Optional[str] = None
    curso_id: Optional[int] = None


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: str
    objetivo: Optional[str] = None
    curso_id: Optional[int] = None


class InteresseIn(BaseModel):
    area_id: int


class GapItem(BaseModel):
    area_nome: str
    disciplinas_ja_cursadas: List[str]
    disciplinas_recomendadas: List[str]
    compatibilidade_percentual: float


class RecomendacaoOut(BaseModel):
    area: AreaOut
    compatibilidade_percentual: float
    disciplinas_relacionadas_cursadas: List[str]
    trilha_sugerida: List[EtapaTrilhaOut] = []
    cursos_complementares: List[CursoComplementarOut] = []
    pos_graduacoes: List[PosGraduacaoOut] = []
    justificativa: str
