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
    origem: Optional[str] = None


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


# ---------------------------------------------------------------------------
# Upload e análise de PPC real (PDF) — seção 28
# ---------------------------------------------------------------------------

class DisciplinaExtraidaIn(BaseModel):
    """Uma disciplina extraída (ou editada manualmente) na etapa de revisão."""
    nome: str
    semestre: int
    carga_horaria: Optional[int] = None
    ementa: Optional[str] = None


class CursoSugeridoOut(BaseModel):
    nome_curso: Optional[str] = None
    instituicao: Optional[str] = None
    carga_horaria_total: Optional[int] = None
    modalidade: Optional[str] = None


class PPCAnaliseOut(BaseModel):
    """Resposta de /api/ppc/analisar — uma prévia, nada é salvo ainda."""
    metodo_extracao: str
    avisos: List[str] = []
    curso_sugerido: CursoSugeridoOut
    disciplinas: List[DisciplinaExtraidaIn]
    areas_relevantes: List[str] = []


class PPCConfirmarIn(BaseModel):
    """Corpo de /api/ppc/confirmar — o que o usuário revisou/editou na tela."""
    nome_curso: str
    instituicao: Optional[str] = "Instituição não informada"
    carga_horaria_total: Optional[int] = None
    modalidade: Optional[str] = None
    disciplinas: List[DisciplinaExtraidaIn]


# ---------------------------------------------------------------------------
# Formações reais (busca ao vivo) — pedido do usuário: cursos reais,
# onde fazer, período de inscrição
# ---------------------------------------------------------------------------

class FormacaoRealOut(BaseModel):
    tipo: str  # graduacao | curso_livre | pos_graduacao
    titulo: str
    instituicao_provavel: Optional[str] = None
    modalidade: Optional[str] = None
    periodo_inscricao: Optional[str] = None
    resumo: Optional[str] = None
    fonte_url: str


class FormacoesReaisOut(BaseModel):
    area: str
    estado: Optional[str] = None
    formacoes: List[FormacaoRealOut] = []
    erro: Optional[str] = None
