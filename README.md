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
  curricular automaticamente (`ppc_parser.py` — tenta ler tabelas primeiro,
  cai para heurística de texto se não encontrar), com uma etapa de revisão
  editável antes de confirmar (a extração de PDF nunca é 100% confiável,
  então o fluxo já assume que o usuário vai corrigir).
- **Classificação automática de disciplina → área** (`area_classifier.py`):
  como um PPC real não tem curadoria manual, cada disciplina extraída é
  comparada por palavras-chave contra ~19 áreas de conhecimento
  (`area_data.py`) — cobre não só TI, mas também Direito, Saúde, Educação,
  Engenharias, Design, Administração etc., já que o PPC pode ser de
  qualquer curso.
- **Dados de exemplo** continuam disponíveis como atalho de demonstração: o
  curso de "Tecnologia em Sistemas para Internet" com 15 disciplinas.
- **Motor de recomendação** (seções 14, 30-31): calcula compatibilidade
  percentual entre o curso do estudante e uma área de interesse.
- **Gap analysis** (seção 15): o que já foi cursado x o que falta.
- **Dashboard** (seção 33): compatibilidade em todas as áreas de uma vez.
- **Formações reais via busca ao vivo**: para a área escolhida, o sistema
  busca ao vivo na web (`web_search.py`, sem precisar de chave de API paga)
  por graduações, cursos livres e pós-graduações reais relacionados,
  tentando identificar instituição, modalidade e período de inscrição —
  sempre citando a fonte, já que é uma extração de texto livre e pode
  falhar ou ficar desatualizada.
- **Front-end redesenhado**: fluxo em trilha vertical (Envie o PPC → Revise
  a grade → Compatibilidade → Sua trilha + formações reais), com cada etapa
  se desbloqueando conforme a anterior é concluída.

## O que NÃO está implementado ainda (propositalmente)

- Autenticação real (login/senha com hash seguro) — hoje o cadastro de
  usuário existe (`POST /api/usuarios`) mas sem hash de verdade nem sessão.
- Machine Learning / NLP (seção 29) — o motor de recomendação é baseado em
  pontuação por conteúdo, como o próprio documento recomenda para começar.
  A classificação de disciplina→área do PPC também é por palavra-chave, não
  por modelo de linguagem — deliberado, para manter o sistema auditável e
  sem depender de API paga.
- A busca de formações reais usa a versão HTML gratuita do DuckDuckGo (sem
  chave de API). É mais frágil e mais lenta que o resto do sistema — para
  produção séria, trocar por uma API de busca paga (Serper, Tavily, Bing)
  deixaria isso mais estável. A troca é isolada em `web_search.py`.

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
pular direto para o dashboard.

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
    └── index.html              # trilha vertical: upload → revisão → dashboard → trilha (HTML/CSS/JS puro)
```

## Endpoints principais

| Método | Rota | O que faz |
|---|---|---|
| POST | `/api/ppc/analisar` | Recebe o PPC (PDF), devolve prévia da extração (nada é salvo) |
| POST | `/api/ppc/confirmar` | Salva o curso + disciplinas revisadas pelo usuário |
| GET | `/api/cursos` | Lista cursos cadastrados |
| GET | `/api/cursos/{id}/disciplinas` | Grade curricular do curso |
| GET | `/api/areas` | Lista as áreas de conhecimento |
| GET | `/api/cursos/{id}/dashboard` | Compatibilidade em todas as áreas |
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
