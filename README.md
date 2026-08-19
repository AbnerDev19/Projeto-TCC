# Trilha Acadêmica — Protótipo funcional (Nível 1 + Nível 2 + parte do Nível 3)

Este é um protótipo **testável de verdade** da estrutura completa descrita no
planejamento do TCC: banco de dados relacional, API (FastAPI) e front-end
consumindo a API. Implementa o "Nível 1" (obrigatório), o "Nível 2"
(recomendação personalizada + gap analysis) e parte do "Nível 3"
(importação automática de PPC real em PDF — seção 28), conforme a seção 49
do documento.

## O que já funciona

- **Banco de dados** com o esquema da seção 24: instituições, cursos,
  disciplinas, áreas, relação N:N disciplina↔área (seção 25), usuários,
  interesses, cursos complementares, pós-graduações, trilhas e etapas.
- **Upload real de PPC em PDF** (seção 28): o usuário envia o Projeto
  Pedagógico de Curso da própria instituição e o sistema extrai a matriz
  curricular automaticamente. `ppc_parser.py` tenta ler tabelas primeiro,
  cai para heurística de texto se não encontrar, e ainda tenta casar cada
  disciplina com um **ementário** (seção comum em PPCs brasileiros) para
  trazer a descrição real do conteúdo — não só o nome. Uma tela de revisão
  editável antecede a confirmação, já que a extração nunca é 100% confiável.
- **Tela de análise em tempo real**: enquanto o PDF é processado, o
  front-end mostra um painel com spinner e mensagens de progresso
  ("Lendo o PDF…", "Procurando o ementário…" etc.), em vez de deixar o
  usuário sem retorno visual.
- **Classificação automática de disciplina → área** (`area_classifier.py`):
  como um PPC real não tem curadoria manual, cada disciplina extraída é
  comparada por palavras-chave (com correspondência por palavra inteira,
  não substring) contra ~19 áreas de conhecimento (`area_data.py`) — cobre
  não só TI, mas também Direito, Saúde, Educação, Engenharias, Design,
  Administração etc.
- **Disciplinas em cards** (em vez de um dashboard de compatibilidade que
  o usuário precisaria escolher): cada disciplina da grade vira um card
  com ementa, carga horária, um checkbox para marcar **"já concluí esta
  matéria"** (persistido no banco) e sugestões de **cursos gratuitos
  curados e verificados** relacionados àquela disciplina especificamente
  (`area_data.py` — Fundação Bradesco, Curso em Vídeo, UNA-SUS, Sebrae,
  Cisco Networking Academy, AWS Skill Builder etc., sempre com link real).
- **Árvore de trilha pós-formação**: a partir das áreas realmente
  relacionadas às disciplinas do curso, o sistema monta uma árvore
  ramificada — cada área é um ramo que o estudante pode abrir para ver
  pós-graduação cadastrada, cursos gratuitos e, sob demanda, uma busca ao
  vivo por formações reais (graduação, cursos livres, pós-graduação) com
  instituição, modalidade e período de inscrição quando encontrados.
- **Motor de recomendação** (seções 14, 30-31): calcula compatibilidade
  percentual entre o curso do estudante e uma área de interesse — hoje
  usado como informação auxiliar (badge de % em cada ramo da árvore), não
  mais como filtro obrigatório antes de ver a trilha.
- **Gap analysis** (seção 15): o que já foi cursado x o que falta,
  disponível via API (`/api/cursos/{id}/gap/{area_id}`).
- **Formações reais via busca ao vivo**: busca ao vivo na web
  (`web_search.py`, sem precisar de chave de API paga) por graduações,
  cursos livres e pós-graduações reais, tentando identificar instituição,
  modalidade e período de inscrição — sempre citando a fonte.

## O que NÃO está implementado ainda (propositalmente)

- Autenticação real (login/senha com hash seguro) — hoje o cadastro de
  usuário existe (`POST /api/usuarios`) mas sem hash de verdade nem sessão.
- Machine Learning / NLP (seção 29) — tanto o motor de recomendação quanto
  o classificador de disciplina→área são baseados em pontuação por
  palavra-chave, não em modelo de linguagem — deliberado, para manter o
  sistema auditável e sem depender de API paga.
- A busca de formações reais usa a versão HTML gratuita do DuckDuckGo (sem
  chave de API). É mais frágil e mais lenta que o resto do sistema — para
  produção séria, trocar por uma API de busca paga (Serper, Tavily, Bing)
  deixaria isso mais estável. A troca é isolada em `web_search.py`.
- A lista de cursos gratuitos por área (`area_data.py`) é curada à mão e
  deve ser revisada periodicamente — catálogos de curso mudam com o tempo.
- A extração de ementário funciona bem com PPCs que têm uma seção clara de
  "Ementário"/"Ementas" — PPCs sem essa seção, ou com layout muito
  diferente, não vão preencher a ementa automaticamente (o card mostra
  "Ementa não identificada" nesses casos, sem quebrar o fluxo).

## Como rodar localmente

```bash
cd backend
pip install -r requirements.txt

# popula o banco (SQLite local, arquivo trilha_academica.db) com o curso
# de demonstração — opcional, o fluxo principal agora é enviar um PPC real
python -m app.seed

# sobe a API + serve o front-end na mesma porta
python -m uvicorn app.main:app --reload --port 8000
```

Depois abra **http://localhost:8000** no navegador — o front-end já vem
junto, servido pelo próprio FastAPI. Envie um PPC real em PDF na primeira
etapa, ou clique em "veja como funciona com um curso de demonstração" para
pular direto para os cards de disciplina.

A documentação interativa da API (gerada automaticamente) fica em
**http://localhost:8000/docs**.

## Deploy em produção (Railway — grátis)

O projeto já está pronto pra isso: tem `Dockerfile`, detecta `DATABASE_URL`
automaticamente e popula o banco sozinho no primeiro start.

1. **Suba o código pro GitHub.**
   ```bash
   cd trilha-academica
   git init
   git add .
   git commit -m "primeiro commit"
   ```
   Crie um repositório vazio no GitHub (github.com/new) e depois:
   ```bash
   git remote add origin https://github.com/SEU_USUARIO/trilha-academica.git
   git branch -M main
   git push -u origin main
   ```

2. **Crie a conta no Railway.** Entre em [railway.app](https://railway.app)
   e faça login com sua conta do GitHub (não precisa cartão pro free tier).

3. **Novo projeto → Deploy from GitHub repo.** Selecione o repositório
   `trilha-academica`. O Railway vai detectar o `Dockerfile` sozinho e
   começar o build.

4. **Adicione o banco Postgres:** dentro do projeto, clique em
   **+ New → Database → PostgreSQL**. O Railway já injeta a variável
   `DATABASE_URL` automaticamente no seu serviço — não precisa configurar
   nada manualmente, o `database.py` já está preparado pra ler essa
   variável.

5. **Gere o domínio público:** no serviço do back-end, vá em
   **Settings → Networking → Generate Domain**. Isso te dá uma URL tipo
   `trilha-academica-production.up.railway.app`.

6. **Pronto.** Acesse a URL gerada — o front-end e a API já estão no ar
   juntos. Na primeira requisição, o banco Postgres é populado
   automaticamente com os dados de exemplo (o mesmo `seed.py` que roda
   localmente).

Cada novo `git push` pra branch `main` gera um novo deploy automático.

### Se quiser trocar os dados de exemplo por dados reais depois

Edite `backend/app/seed.py` com as disciplinas do seu curso real, apague
a tabela `cursos` no Postgres (pelo painel do Railway, aba **Data**) e
reinicie o serviço — o seed roda de novo sozinho.

## Como trocar para PostgreSQL localmente (fora do Railway)

Se quiser testar com Postgres na sua máquina antes de subir:

```bash
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/trilha_academica"
```


## Estrutura de pastas

```
trilha-academica/
├── backend/
│   ├── app/
│   │   ├── main.py             # rotas da API (FastAPI)
│   │   ├── models.py           # modelos SQLAlchemy (esquema da seção 24)
│   │   ├── schemas.py          # schemas Pydantic (validação/serialização)
│   │   ├── recommendation.py   # motor de recomendação (seções 30-31)
│   │   ├── ppc_parser.py       # extração heurística de PPC real em PDF (seção 28)
│   │   ├── area_classifier.py  # classificação automática disciplina -> área
│   │   ├── area_data.py        # definição das ~19 áreas + palavras-chave
│   │   ├── web_search.py       # busca ao vivo de formações reais na web
│   │   ├── seed.py             # dados de exemplo (curso, disciplinas, áreas)
│   │   └── database.py         # conexão com o banco (SQLite -> Postgres)
│   └── requirements.txt
└── frontend/
    └── index.html              # trilha vertical: upload → revisão → cards de disciplina → árvore (HTML/CSS/JS puro)
```

## Endpoints principais

| Método | Rota | O que faz |
|---|---|---|
| POST | `/api/ppc/analisar` | Recebe o PPC (PDF), devolve prévia da extração (nada é salvo) |
| POST | `/api/ppc/confirmar` | Salva o curso + disciplinas revisadas pelo usuário |
| GET | `/api/cursos` | Lista cursos cadastrados |
| GET | `/api/cursos/{id}/disciplinas` | Grade curricular do curso, com áreas e status de conclusão |
| PATCH | `/api/disciplinas/{id}/concluida` | Marca/desmarca uma disciplina como já concluída |
| GET | `/api/areas` | Lista as áreas de conhecimento |
| GET | `/api/areas/{id}/cursos-gratuitos` | Lista curada de cursos gratuitos reais para a área |
| GET | `/api/cursos/{id}/arvore` | Árvore de trilha pós-formação: um ramo por área relevante |
| GET | `/api/cursos/{id}/dashboard` | Compatibilidade em todas as áreas (auxiliar, não gatilho do fluxo) |
| GET | `/api/cursos/{id}/recomendacao/{area_id}` | Trilha + justificativa para uma área |
| GET | `/api/cursos/{id}/gap/{area_id}` | O que já foi cursado x o que falta |
| GET | `/api/cursos/{id}/formacoes-reais/{area_id}` | Busca ao vivo: graduação, cursos livres e pós reais |
| POST | `/api/usuarios` | Cadastro de estudante |

## Próximos passos sugeridos

1. Trocar o SQLite pelo PostgreSQL (só muda `DATABASE_URL`).
2. Implementar autenticação real (JWT + hash de senha com `passlib`).
3. Permitir que o estudante selecione seus interesses e objetivo (seção 13)
   e salvar isso no banco (`interesses_usuario`).
4. Trocar a busca gratuita do DuckDuckGo por uma API de busca paga (Serper,
   Tavily, Bing) para tornar a busca de formações reais mais estável e
   rápida em produção — a troca fica isolada em `web_search.py`.
5. Melhorar a extração de PPCs com layouts muito fora do padrão (ex.:
   PDFs escaneados como imagem, que exigiriam OCR).
