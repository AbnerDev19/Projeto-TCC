# Trilha Acadêmica — Protótipo funcional (Nível 1 + parte do Nível 2)

Este é um protótipo **testável de verdade** da estrutura completa descrita no
planejamento do TCC: banco de dados relacional, API (FastAPI) e front-end
básico consumindo a API. Já implementa o "Nível 1" (obrigatório) e parte do
"Nível 2" (recomendação personalizada + gap analysis), conforme a seção 49
do documento.

## O que já funciona

- **Banco de dados** com o esquema da seção 24: instituições, cursos,
  disciplinas, áreas, relação N:N disciplina↔área (seção 25), usuários,
  interesses, cursos complementares, pós-graduações, trilhas e etapas.
- **Dados de exemplo** já carregados: o curso de "Tecnologia em Sistemas
  para Internet" com 15 disciplinas (as mesmas citadas no exemplo do
  documento, seção 11) e 10 áreas de conhecimento (seção 12).
- **Motor de recomendação** (seções 14, 30-31): calcula compatibilidade
  percentual entre o curso do estudante e uma área de interesse, com base em
  pesos disciplina→área.
- **Gap analysis** (seção 15): mostra o que já foi cursado x o que falta
  para a área escolhida.
- **Dashboard** (seção 33): compatibilidade em todas as áreas de uma vez.
- **Front-end básico**: uma página que consome a API, mostra o dashboard em
  barras e, ao clicar numa área, gera a trilha visual (seção 34), a análise
  de lacunas, cursos complementares e pós-graduações recomendadas.

## O que NÃO está implementado ainda (propositalmente)

- Autenticação real (login/senha com hash seguro) — hoje o cadastro de
  usuário existe (`POST /api/usuarios`) mas sem hash de verdade nem sessão.
- Importação automática de PPC em PDF (seção 28) — os dados são inseridos
  via `seed.py`, simulando o que viria de um PPC já processado.
- Machine Learning / NLP (seção 29) — o motor de recomendação é baseado em
  pontuação por conteúdo, como o próprio documento recomenda para começar.

Essas partes são o próximo passo natural depois que a estrutura base (que
você pediu para testar) estiver validada.

## Como rodar localmente

```bash
cd backend
pip install -r requirements.txt

# popula o banco (SQLite local, arquivo trilha_academica.db)
python -m app.seed

# sobe a API + serve o front-end na mesma porta
python -m uvicorn app.main:app --reload --port 8000
```

Depois abra **http://localhost:8000** no navegador — o front-end já vem
junto, servido pelo próprio FastAPI.

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
│   │   ├── main.py            # rotas da API (FastAPI)
│   │   ├── models.py          # modelos SQLAlchemy (esquema da seção 24)
│   │   ├── schemas.py         # schemas Pydantic (validação/serialização)
│   │   ├── recommendation.py  # motor de recomendação (seções 30-31)
│   │   ├── seed.py            # dados de exemplo (curso, disciplinas, áreas)
│   │   └── database.py        # conexão com o banco (SQLite -> Postgres)
│   └── requirements.txt
└── frontend/
    └── index.html             # dashboard + trilha (HTML/CSS/JS puro)
```

## Endpoints principais

| Método | Rota | O que faz |
|---|---|---|
| GET | `/api/cursos` | Lista cursos cadastrados |
| GET | `/api/cursos/{id}/disciplinas` | Grade curricular do curso |
| GET | `/api/areas` | Lista as áreas de conhecimento |
| GET | `/api/cursos/{id}/dashboard` | Compatibilidade em todas as áreas |
| GET | `/api/cursos/{id}/recomendacao/{area_id}` | Trilha + justificativa para uma área |
| GET | `/api/cursos/{id}/gap/{area_id}` | O que já foi cursado x o que falta |
| POST | `/api/usuarios` | Cadastro de estudante |

## Próximos passos sugeridos

1. Trocar o SQLite pelo PostgreSQL (só muda `DATABASE_URL`).
2. Implementar autenticação real (JWT + hash de senha com `passlib`).
3. Permitir que o estudante selecione seus interesses e objetivo (seção 13)
   e salvar isso no banco (`interesses_usuario`).
4. Testar a extração de um PPC real em PDF (seção 28) — dá pra começar com
   extração manual assistida (o sistema já suporta cadastro manual).
