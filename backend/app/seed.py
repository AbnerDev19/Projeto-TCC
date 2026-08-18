"""
Popula o banco com dados de exemplo — o mesmo cenário usado no documento
do TCC (seções 11, 12, 14): curso de Tecnologia em Sistemas para Internet.
Rodar com: python -m app.seed
"""
from .database import Base, engine, SessionLocal
from . import models

#            nome, descrição, pontos_ideais (nível de domínio esperado na área)
AREAS = [
    ("Desenvolvimento Web", "Construção de aplicações e sistemas para a web.", 9),
    ("Engenharia de Software", "Processos, arquitetura e qualidade de software.", 12),
    ("Banco de Dados", "Modelagem, armazenamento e consulta de dados.", 8),
    ("Ciência de Dados", "Análise, estatística e extração de conhecimento a partir de dados.", 13),
    ("Inteligência Artificial", "Aprendizado de máquina, IA e automação de decisões.", 12),
    ("Redes", "Infraestrutura, protocolos e comunicação de dados.", 7),
    ("Segurança da Informação", "Proteção de dados, sistemas e infraestrutura.", 8),
    ("Computação em Nuvem", "Infraestrutura, deploy e escalabilidade em nuvem.", 7),
    ("Gestão de Tecnologia", "Gestão de projetos, produtos e equipes de TI.", 9),
    ("Pesquisa Acadêmica", "Iniciação científica, pesquisa e produção acadêmica.", 5),
]

# nome, semestre, carga_horaria, ementa
DISCIPLINAS = [
    ("Algoritmos", 1, 80, "Lógica de programação, estruturas de controle, resolução de problemas."),
    ("Introdução à Computação", 1, 40, "História da computação, hardware, software, fundamentos."),
    ("Matemática", 1, 80, "Funções, matemática discreta aplicada à computação."),
    ("Banco de Dados", 2, 80, "Modelagem relacional, SQL, normalização, banco de dados."),
    ("Programação Orientada a Objetos", 2, 80, "Classes, herança, polimorfismo, encapsulamento."),
    ("Desenvolvimento Web", 2, 80, "HTML, CSS, JavaScript, front-end e back-end para web."),
    ("Estrutura de Dados", 3, 80, "Listas, pilhas, filas, árvores, grafos, complexidade."),
    ("Redes de Computadores", 3, 60, "Protocolos, arquitetura de redes, TCP/IP."),
    ("Engenharia de Software", 4, 80, "Processos de desenvolvimento, requisitos, metodologias ágeis."),
    ("Estatística Aplicada", 4, 60, "Probabilidade, estatística descritiva e inferencial."),
    ("Segurança da Informação", 5, 60, "Criptografia, vulnerabilidades, boas práticas de segurança."),
    ("Computação em Nuvem", 5, 60, "Infraestrutura como serviço, containers, deploy em nuvem."),
    ("Inteligência Artificial", 6, 60, "Fundamentos de IA, aprendizado de máquina, redes neurais."),
    ("Gestão de Projetos de TI", 6, 40, "Planejamento, times, metodologias de gestão de projetos."),
    ("Trabalho de Conclusão de Curso I", 6, 40, "Metodologia científica e elaboração de projeto de pesquisa."),
]

# nome_disciplina -> [(nome_area, peso)]
DISCIPLINA_AREA = {
    "Algoritmos": [("Engenharia de Software", 2), ("Desenvolvimento Web", 1)],
    "Introdução à Computação": [("Gestão de Tecnologia", 1)],
    "Matemática": [("Ciência de Dados", 1), ("Inteligência Artificial", 1)],
    "Banco de Dados": [("Banco de Dados", 3), ("Ciência de Dados", 2), ("Engenharia de Software", 1)],
    "Programação Orientada a Objetos": [("Engenharia de Software", 3), ("Desenvolvimento Web", 2)],
    "Desenvolvimento Web": [("Desenvolvimento Web", 3), ("Engenharia de Software", 1)],
    "Estrutura de Dados": [("Engenharia de Software", 2), ("Ciência de Dados", 1), ("Inteligência Artificial", 1)],
    "Redes de Computadores": [("Redes", 3), ("Segurança da Informação", 1), ("Computação em Nuvem", 1)],
    "Engenharia de Software": [("Engenharia de Software", 3), ("Gestão de Tecnologia", 1)],
    "Estatística Aplicada": [("Ciência de Dados", 3), ("Inteligência Artificial", 1)],
    "Segurança da Informação": [("Segurança da Informação", 3), ("Redes", 1)],
    "Computação em Nuvem": [("Computação em Nuvem", 3), ("Redes", 1), ("Gestão de Tecnologia", 1)],
    "Inteligência Artificial": [("Inteligência Artificial", 3), ("Ciência de Dados", 2)],
    "Gestão de Projetos de TI": [("Gestão de Tecnologia", 3)],
    "Trabalho de Conclusão de Curso I": [("Pesquisa Acadêmica", 3)],
}

CURSOS_COMPLEMENTARES = [
    ("Python para Ciência de Dados", "Ciência de Dados", "Online", 40),
    ("Fundamentos de Machine Learning", "Inteligência Artificial", "Online", 60),
    ("SQL Avançado", "Banco de Dados", "Online", 30),
    ("Introdução ao Docker e Kubernetes", "Computação em Nuvem", "Online", 40),
    ("Pentest e Segurança Ofensiva", "Segurança da Informação", "Online", 50),
    ("React do Zero ao Avançado", "Desenvolvimento Web", "Online", 45),
]

POS_GRADUACOES = [
    ("Especialização em Ciência de Dados", "especializacao", "Engenharia de Software"),
    ("Especialização em Engenharia de Software", "especializacao", "Engenharia de Software"),
    ("Especialização em Segurança da Informação", "especializacao", "Segurança da Informação"),
    ("Mestrado em Computação Aplicada", "mestrado", "Inteligência Artificial"),
    ("Mestrado em Ciência da Computação", "mestrado", "Ciência de Dados"),
]

TRILHA_CIENCIA_DE_DADOS = [
    (1, "Banco de Dados", "Banco de Dados (já cursada)"),
    (2, "Python", "Python para Ciência de Dados"),
    (3, "Estatística", "Estatística Aplicada (já cursada)"),
    (4, "Análise de Dados", "Curso livre de Análise de Dados"),
    (5, "Machine Learning", "Fundamentos de Machine Learning"),
    (6, "Projeto de pesquisa", "TCC com foco em dados"),
    (7, "Especialização em Ciência de Dados", None),
    (8, "Mestrado em Computação", None),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Curso).first():
            print("Banco já populado, pulando seed.")
            return

        inst = models.Instituicao(nome="Instituto Exemplo de Tecnologia", cidade="Brasília", estado="DF")
        db.add(inst)
        db.flush()

        curso = models.Curso(
            nome="Tecnologia em Sistemas para Internet",
            instituicao_id=inst.id,
            carga_horaria=2400,
            duracao_semestres=6,
            modalidade="Presencial",
        )
        db.add(curso)
        db.flush()

        areas_map = {}
        for nome, desc, pontos_ideais in AREAS:
            a = models.Area(nome=nome, descricao=desc, pontos_ideais=pontos_ideais)
            db.add(a)
            db.flush()
            areas_map[nome] = a

        disciplinas_map = {}
        for nome, semestre, ch, ementa in DISCIPLINAS:
            d = models.Disciplina(nome=nome, semestre=semestre, carga_horaria=ch, ementa=ementa, curso_id=curso.id)
            db.add(d)
            db.flush()
            disciplinas_map[nome] = d

        for disc_nome, relacoes in DISCIPLINA_AREA.items():
            disc = disciplinas_map[disc_nome]
            for area_nome, peso in relacoes:
                db.execute(
                    models.disciplina_area.insert().values(
                        disciplina_id=disc.id, area_id=areas_map[area_nome].id, peso=peso
                    )
                )

        for nome, area_nome, modalidade, ch in CURSOS_COMPLEMENTARES:
            db.add(models.CursoComplementar(
                nome=nome, instituicao="Plataforma Parceira", modalidade=modalidade,
                carga_horaria=ch, area_id=areas_map[area_nome].id,
            ))

        for nome, tipo, area_nome in POS_GRADUACOES:
            db.add(models.PosGraduacao(
                nome=nome, tipo=tipo, instituicao="Instituto Exemplo de Tecnologia",
                area_id=areas_map[area_nome].id, modalidade="Híbrido",
            ))

        trilha = models.Trilha(nome="Trilha de Ciência de Dados", area_id=areas_map["Ciência de Dados"].id)
        db.add(trilha)
        db.flush()
        for ordem, conhecimento, curso_sugerido in TRILHA_CIENCIA_DE_DADOS:
            db.add(models.EtapaTrilha(
                trilha_id=trilha.id, ordem=ordem, conhecimento=conhecimento,
                curso_sugerido=curso_sugerido, area_id=areas_map["Ciência de Dados"].id,
            ))

        db.commit()
        print(f"Seed concluído: curso '{curso.nome}' (id={curso.id}) com {len(DISCIPLINAS)} disciplinas e {len(AREAS)} áreas.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
