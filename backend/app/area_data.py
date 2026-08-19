"""
Definição das áreas de conhecimento usadas em todo o sistema.

Cada área carrega:
  - descricao / pontos_ideais: usados pelo motor de recomendação (recommendation.py)
  - keywords: usadas pelo classificador automático (area_classifier.py) para
    associar uma disciplina extraída de um PPC real a uma ou mais áreas, sem
    depender de curadoria manual (que só existe para o curso de demonstração).
  - cursos_gratuitos: uma pequena lista curada de plataformas REAIS e
    genuinamente gratuitas (verificadas), usada nos cards de disciplina e na
    árvore de trilha. Diferente das "formações reais" (que vêm de busca ao
    vivo e podem ser pagas, como graduação e pós), esta lista é sempre
    gratuita — por isso é curada à mão em vez de buscada, e deve ser revisada
    periodicamente já que catálogos de curso mudam com o tempo.
"""

AREA_DEFINICOES = {
    "Desenvolvimento Web": {
        "descricao": "Construção de aplicações e sistemas para a web.",
        "pontos_ideais": 9,
        "keywords": [
            "desenvolvimento web", "html", "css", "javascript", "front-end",
            "frontend", "back-end", "backend", "framework web", "aplicacao web",
            "programacao web", "react", "node", "api rest", "responsivo",
        ],
        "cursos_gratuitos": [
            {"nome": "HTML5, CSS3 e JavaScript", "plataforma": "Curso em Vídeo", "url": "https://www.cursoemvideo.com",
             "descricao": "Aulas em vídeo gratuitas, do zero ao intermediário em front-end, com o professor Gustavo Guanabara."},
            {"nome": "Responsive Web Design", "plataforma": "freeCodeCamp", "url": "https://www.freecodecamp.org",
             "descricao": "Currículo interativo e gratuito de HTML e CSS, com certificado gratuito ao final."},
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
        "cursos_gratuitos": [
            {"nome": "Lógica de Programação e Algoritmos", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Curso introdutório gratuito com certificado digital sobre lógica e estruturas de programação."},
            {"nome": "Algoritmos", "plataforma": "Curso em Vídeo", "url": "https://www.cursoemvideo.com",
             "descricao": "Aulas gratuitas sobre lógica de programação e algoritmos do zero."},
        ],
    },
    "Banco de Dados": {
        "descricao": "Modelagem, armazenamento e consulta de dados.",
        "pontos_ideais": 8,
        "keywords": [
            "banco de dados", "sql", "modelagem de dados", "normalizacao",
            "sistema gerenciador de banco de dados", "sgbd", "nosql", "consulta a dados",
        ],
        "cursos_gratuitos": [
            {"nome": "MySQL e Banco de Dados", "plataforma": "Curso em Vídeo", "url": "https://www.cursoemvideo.com",
             "descricao": "Curso gratuito em vídeo sobre modelagem relacional e consultas SQL."},
            {"nome": "Tecnologia da Informação", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Trilha gratuita com cursos introdutórios de TI, incluindo fundamentos de banco de dados."},
        ],
    },
    "Ciência de Dados": {
        "descricao": "Análise, estatística e extração de conhecimento a partir de dados.",
        "pontos_ideais": 13,
        "keywords": [
            "ciencia de dados", "estatistica", "probabilidade", "mineracao de dados",
            "analise de dados", "big data", "visualizacao de dados", "data science",
        ],
        "cursos_gratuitos": [
            {"nome": "Micro-cursos de Python e Dados", "plataforma": "Kaggle Learn", "url": "https://www.kaggle.com/learn",
             "descricao": "Cursos curtos, práticos e gratuitos de Python, pandas e machine learning, direto no navegador."},
            {"nome": "Trilha de Inteligência Artificial e Dados", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Trilha gratuita sobre IA e dados, em parceria com a Microsoft."},
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
        "cursos_gratuitos": [
            {"nome": "Elements of AI", "plataforma": "Universidade de Helsinque", "url": "https://www.elementsofai.com",
             "descricao": "Curso introdutório gratuito e traduzido sobre IA, sem pré-requisitos técnicos."},
            {"nome": "FluêncIA — IA generativa e Copilot", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Trilha gratuita sobre IA generativa, em parceria com a Microsoft."},
        ],
    },
    "Redes": {
        "descricao": "Infraestrutura, protocolos e comunicação de dados.",
        "pontos_ideais": 7,
        "keywords": [
            "redes de computadores", "protocolo", "tcp/ip", "infraestrutura de redes",
            "telecomunicacoes", "comunicacao de dados",
        ],
        "cursos_gratuitos": [
            {"nome": "Introduction to Networks", "plataforma": "Cisco Networking Academy", "url": "https://www.netacad.com",
             "descricao": "Curso introdutório gratuito de redes de computadores da Cisco, com certificado."},
            {"nome": "Tecnologia da Informação", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Cursos gratuitos introdutórios de infraestrutura de TI."},
        ],
    },
    "Segurança da Informação": {
        "descricao": "Proteção de dados, sistemas e infraestrutura.",
        "pontos_ideais": 8,
        "keywords": [
            "seguranca da informacao", "criptografia", "vulnerabilidade", "pentest",
            "seguranca cibernetica", "auditoria de seguranca", "firewall",
        ],
        "cursos_gratuitos": [
            {"nome": "Introduction to Cybersecurity", "plataforma": "Cisco Networking Academy", "url": "https://www.netacad.com",
             "descricao": "Curso introdutório gratuito sobre ameaças e boas práticas de segurança digital."},
            {"nome": "Segurança da Informação", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Curso gratuito introdutório sobre proteção de dados, com certificado."},
        ],
    },
    "Computação em Nuvem": {
        "descricao": "Infraestrutura, deploy e escalabilidade em nuvem.",
        "pontos_ideais": 7,
        "keywords": [
            "computacao em nuvem", "cloud", "docker", "kubernetes", "devops",
            "infraestrutura como servico", "containers",
        ],
        "cursos_gratuitos": [
            {"nome": "AWS Cloud Practitioner Essentials", "plataforma": "AWS Skill Builder", "url": "https://skillbuilder.aws",
             "descricao": "Curso introdutório gratuito da própria Amazon sobre fundamentos de nuvem."},
            {"nome": "Microsoft Azure Fundamentals", "plataforma": "Microsoft Learn", "url": "https://learn.microsoft.com",
             "descricao": "Trilha gratuita e oficial da Microsoft sobre fundamentos de computação em nuvem."},
        ],
    },
    "Gestão de Tecnologia": {
        "descricao": "Gestão de projetos, produtos e equipes de TI.",
        "pontos_ideais": 9,
        "keywords": [
            "gestao de projetos", "gestao de ti", "gerenciamento de projetos",
            "governanca de ti", "gestao de produtos", "lideranca de equipes de tecnologia",
        ],
        "cursos_gratuitos": [
            {"nome": "Gestão de Projetos", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Curso gratuito introdutório sobre planejamento e gestão de projetos."},
            {"nome": "Gestão de Processos", "plataforma": "Sebrae", "url": "https://loja.sebrae.com.br",
             "descricao": "Curso curto e gratuito sobre organização e melhoria de processos, com certificado digital."},
        ],
    },
    "Pesquisa Acadêmica": {
        "descricao": "Iniciação científica, pesquisa e produção acadêmica.",
        "pontos_ideais": 5,
        "keywords": [
            "metodologia cientifica", "trabalho de conclusao de curso", "iniciacao cientifica",
            "pesquisa academica", "producao academica", "tcc",
        ],
        "cursos_gratuitos": [
            {"nome": "Metodologias de Aprendizagem", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Cursos gratuitos sobre metodologias de estudo e produção de conteúdo."},
            {"nome": "Pesquisa científica e revisão bibliográfica", "plataforma": "UNA-SUS / Ebserh", "url": "https://www.unasus.gov.br",
             "descricao": "Vídeos curtos e gratuitos sobre metodologia científica, gerenciadores de referência e escrita acadêmica."},
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
        "cursos_gratuitos": [
            {"nome": "Trilha de Empreendedorismo", "plataforma": "Sebrae", "url": "https://loja.sebrae.com.br",
             "descricao": "Cursos gratuitos com certificado sobre gestão, planejamento e abertura de negócio."},
            {"nome": "Negócios e Inovação", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Trilha gratuita sobre empreendedorismo, gestão e inovação."},
        ],
    },
    "Contabilidade e Finanças": {
        "descricao": "Contabilidade, controladoria, finanças e mercado de capitais.",
        "pontos_ideais": 9,
        "keywords": [
            "contabilidade", "financas", "controladoria", "custos", "auditoria contabil",
            "mercado de capitais", "analise de investimentos", "tributario",
        ],
        "cursos_gratuitos": [
            {"nome": "Finanças para Pequenos Negócios", "plataforma": "Sebrae", "url": "https://loja.sebrae.com.br",
             "descricao": "Curso gratuito sobre fluxo de caixa e gestão financeira."},
            {"nome": "Contabilidade e Finanças", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Trilha gratuita com cursos introdutórios de contabilidade e educação financeira."},
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
        "cursos_gratuitos": [
            {"nome": "Legislação para empreendedores", "plataforma": "Sebrae", "url": "https://loja.sebrae.com.br",
             "descricao": "Cursos gratuitos sobre formalização de empresas e noções legais básicas."},
            {"nome": "Cursos livres introdutórios", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Cursos gratuitos com noções de legislação e direitos do consumidor."},
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
        "cursos_gratuitos": [
            {"nome": "Cursos livres do SUS", "plataforma": "UNA-SUS", "url": "https://www.unasus.gov.br",
             "descricao": "Centenas de cursos gratuitos com certificado do Ministério da Saúde, para estudantes e profissionais."},
            {"nome": "Atenção Primária à Saúde", "plataforma": "UNA-SUS", "url": "https://www.unasus.gov.br",
             "descricao": "Cursos gratuitos e autoinstrucionais sobre saúde da família e atenção básica."},
        ],
    },
    "Educação": {
        "descricao": "Licenciatura, didática e processos de ensino-aprendizagem.",
        "pontos_ideais": 9,
        "keywords": [
            "didatica", "pratica pedagogica", "psicologia da educacao", "curriculo escolar",
            "metodologia do ensino", "educacao inclusiva", "gestao escolar", "licenciatura",
        ],
        "cursos_gratuitos": [
            {"nome": "Metodologias Ativas e Práticas Pedagógicas", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Cursos gratuitos sobre didática, metodologias de ensino e educação inclusiva."},
            {"nome": "Educação a Distância", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Trilha gratuita sobre metodologias de aprendizagem e ensino híbrido."},
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
        "cursos_gratuitos": [
            {"nome": "Cursos introdutórios de tecnologia e inovação", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Cursos gratuitos aplicáveis a diferentes áreas da engenharia."},
            {"nome": "Cursos de engenharia em modo de auditoria", "plataforma": "Coursera", "url": "https://www.coursera.org",
             "descricao": "Cursos universitários acessíveis gratuitamente no modo de auditoria (sem certificado pago)."},
        ],
    },
    "Comunicação e Marketing": {
        "descricao": "Comunicação social, publicidade e marketing digital.",
        "pontos_ideais": 9,
        "keywords": [
            "comunicacao social", "publicidade e propaganda", "jornalismo", "marketing digital",
            "redacao publicitaria", "midias sociais", "relacoes publicas", "producao audiovisual",
        ],
        "cursos_gratuitos": [
            {"nome": "Fundamentos de Marketing Digital", "plataforma": "Grow with Google", "url": "https://grow.google",
             "descricao": "Curso gratuito e certificado do Google sobre marketing digital e presença online."},
            {"nome": "Meta Blueprint", "plataforma": "Meta", "url": "https://www.facebook.com/business/learn",
             "descricao": "Cursos gratuitos da Meta sobre marketing em redes sociais e publicidade digital."},
        ],
    },
    "Design": {
        "descricao": "Design gráfico, produto e experiência do usuário.",
        "pontos_ideais": 9,
        "keywords": [
            "design grafico", "design de produto", "experiencia do usuario", "ux",
            "ui design", "design thinking", "tipografia", "design de interacao",
        ],
        "cursos_gratuitos": [
            {"nome": "Canva Design School", "plataforma": "Canva", "url": "https://www.canva.com/designschool",
             "descricao": "Tutoriais e cursos curtos gratuitos sobre fundamentos de design gráfico."},
            {"nome": "Fundamentos de UX Design", "plataforma": "Coursera", "url": "https://www.coursera.org",
             "descricao": "Módulos do certificado de UX Design do Google, acessíveis gratuitamente em modo de auditoria."},
        ],
    },
    "Ciências Humanas e Sociais": {
        "descricao": "Filosofia, sociologia, história e ciências sociais aplicadas.",
        "pontos_ideais": 8,
        "keywords": [
            "sociologia", "filosofia", "historia", "antropologia", "ciencia politica",
            "ciencias sociais", "etica e cidadania",
        ],
        "cursos_gratuitos": [
            {"nome": "Cursos de Humanidades", "plataforma": "Khan Academy", "url": "https://pt.khanacademy.org",
             "descricao": "Cursos gratuitos e em português sobre história, economia e ciências sociais."},
            {"nome": "Desenvolvimento pessoal e cidadania", "plataforma": "Escola Virtual Fundação Bradesco", "url": "https://www.ev.org.br",
             "descricao": "Cursos introdutórios gratuitos sobre desenvolvimento pessoal e ciências sociais aplicadas."},
        ],
    },
}
