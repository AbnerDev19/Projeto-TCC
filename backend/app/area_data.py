"""
Definição das áreas de conhecimento usadas em todo o sistema.

Cada área carrega, além da descrição e da pontuação "ideal" (nível de
domínio esperado — seção 30-31 do documento), uma lista de palavras-chave.
Essas palavras-chave são o que permite classificar automaticamente uma
disciplina extraída de um PPC real (seção 28) sem depender de um mapeamento
manual como o antigo DISCIPLINA_AREA do seed.py — importante porque um PPC
enviado pelo usuário pode ser de qualquer curso, não só o de exemplo.

O conjunto cobre tanto cursos de computação/tecnologia quanto outras
grandes áreas (saúde, direito, negócios, humanas, engenharias, educação
etc.), para que o classificador funcione com PPCs de cursos variados.
"""

# nome -> {"descricao", "pontos_ideais", "keywords"}
# "keywords" usa termos em minúsculas e sem acento (a normalização de
# acentos acontece em area_classifier.py na hora da comparação).
AREA_DEFINICOES = {
    "Desenvolvimento Web": {
        "descricao": "Construção de aplicações e sistemas para a web.",
        "pontos_ideais": 9,
        "keywords": [
            "desenvolvimento web", "html", "css", "javascript", "front-end",
            "frontend", "back-end", "backend", "framework web", "aplicacao web",
            "programacao web", "react", "node", "api rest", "responsivo",
        ],
    },
    "Engenharia de Software": {
        "descricao": "Processos, arquitetura e qualidade de software.",
        "pontos_ideais": 12,
        "keywords": [
            "engenharia de software", "algoritmos", "programacao orientada a objetos",
            "estrutura de dados", "arquitetura de software", "metodologia agil",
            "scrum", "requisitos de software", "teste de software", "qualidade de software",
            "padroes de projeto", "logica de programacao", "poo",
        ],
    },
    "Banco de Dados": {
        "descricao": "Modelagem, armazenamento e consulta de dados.",
        "pontos_ideais": 8,
        "keywords": [
            "banco de dados", "sql", "modelagem de dados", "normalizacao",
            "sistema gerenciador de banco de dados", "sgbd", "nosql", "consulta a dados",
        ],
    },
    "Ciência de Dados": {
        "descricao": "Análise, estatística e extração de conhecimento a partir de dados.",
        "pontos_ideais": 13,
        "keywords": [
            "ciencia de dados", "estatistica", "probabilidade", "mineracao de dados",
            "analise de dados", "big data", "visualizacao de dados", "data science",
        ],
    },
    "Inteligência Artificial": {
        "descricao": "Aprendizado de máquina, IA e automação de decisões.",
        "pontos_ideais": 12,
        "keywords": [
            "inteligencia artificial", "aprendizado de maquina", "machine learning",
            "redes neurais", "deep learning", "processamento de linguagem natural",
            "visao computacional", "sistemas inteligentes",
        ],
    },
    "Redes": {
        "descricao": "Infraestrutura, protocolos e comunicação de dados.",
        "pontos_ideais": 7,
        "keywords": [
            "redes de computadores", "protocolo", "tcp/ip", "infraestrutura de redes",
            "telecomunicacoes", "comunicacao de dados",
        ],
    },
    "Segurança da Informação": {
        "descricao": "Proteção de dados, sistemas e infraestrutura.",
        "pontos_ideais": 8,
        "keywords": [
            "seguranca da informacao", "criptografia", "vulnerabilidade", "pentest",
            "seguranca cibernetica", "auditoria de seguranca", "firewall",
        ],
    },
    "Computação em Nuvem": {
        "descricao": "Infraestrutura, deploy e escalabilidade em nuvem.",
        "pontos_ideais": 7,
        "keywords": [
            "computacao em nuvem", "cloud", "docker", "kubernetes", "devops",
            "infraestrutura como servico", "containers",
        ],
    },
    "Gestão de Tecnologia": {
        "descricao": "Gestão de projetos, produtos e equipes de TI.",
        "pontos_ideais": 9,
        "keywords": [
            "gestao de projetos", "gestao de ti", "gerenciamento de projetos",
            "governanca de ti", "gestao de produtos", "lideranca de equipes de tecnologia",
        ],
    },
    "Pesquisa Acadêmica": {
        "descricao": "Iniciação científica, pesquisa e produção acadêmica.",
        "pontos_ideais": 5,
        "keywords": [
            "metodologia cientifica", "trabalho de conclusao de curso", "iniciacao cientifica",
            "pesquisa academica", "producao academica", "tcc",
        ],
    },
    "Administração e Negócios": {
        "descricao": "Gestão empresarial, empreendedorismo e estratégia de negócios.",
        "pontos_ideais": 10,
        "keywords": [
            "administracao", "gestao empresarial", "empreendedorismo", "estrategia empresarial",
            "marketing", "recursos humanos", "economia", "negocios", "plano de negocios",
            "logistica", "operacoes",
        ],
    },
    "Contabilidade e Finanças": {
        "descricao": "Contabilidade, controladoria, finanças e mercado de capitais.",
        "pontos_ideais": 9,
        "keywords": [
            "contabilidade", "financas", "controladoria", "custos", "auditoria contabil",
            "mercado de capitais", "analise de investimentos", "tributario",
        ],
    },
    "Direito": {
        "descricao": "Ciências jurídicas e prática do direito.",
        "pontos_ideais": 10,
        "keywords": [
            "direito civil", "direito penal", "direito constitucional", "direito administrativo",
            "direito do trabalho", "processo civil", "processo penal", "direito empresarial",
            "etica juridica", "direito tributario",
        ],
    },
    "Saúde": {
        "descricao": "Ciências da saúde, cuidado clínico e saúde pública.",
        "pontos_ideais": 10,
        "keywords": [
            "anatomia", "fisiologia", "saude publica", "farmacologia", "enfermagem",
            "clinica medica", "patologia", "semiologia", "epidemiologia", "nutricao",
            "psicologia clinica", "saude coletiva",
        ],
    },
    "Educação": {
        "descricao": "Licenciatura, didática e processos de ensino-aprendizagem.",
        "pontos_ideais": 9,
        "keywords": [
            "didatica", "pratica pedagogica", "psicologia da educacao", "curriculo escolar",
            "metodologia do ensino", "educacao inclusiva", "gestao escolar", "licenciatura",
        ],
    },
    "Engenharia": {
        "descricao": "Fundamentos e aplicações das engenharias (não computacionais).",
        "pontos_ideais": 11,
        "keywords": [
            "resistencia dos materiais", "mecanica dos solidos", "termodinamica",
            "circuitos eletricos", "calculo estrutural", "processos industriais",
            "engenharia civil", "engenharia mecanica", "engenharia eletrica",
            "engenharia de producao", "hidraulica",
        ],
    },
    "Comunicação e Marketing": {
        "descricao": "Comunicação social, publicidade e marketing digital.",
        "pontos_ideais": 9,
        "keywords": [
            "comunicacao social", "publicidade e propaganda", "jornalismo", "marketing digital",
            "redacao publicitaria", "midias sociais", "relacoes publicas", "producao audiovisual",
        ],
    },
    "Design": {
        "descricao": "Design gráfico, produto e experiência do usuário.",
        "pontos_ideais": 9,
        "keywords": [
            "design grafico", "design de produto", "experiencia do usuario", "ux",
            "ui design", "design thinking", "tipografia", "design de interacao",
        ],
    },
    "Ciências Humanas e Sociais": {
        "descricao": "Filosofia, sociologia, história e ciências sociais aplicadas.",
        "pontos_ideais": 8,
        "keywords": [
            "sociologia", "filosofia", "historia", "antropologia", "ciencia politica",
            "ciencias sociais", "etica e cidadania",
        ],
    },
}
