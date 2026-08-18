# Imagem enxuta com Python
FROM python:3.12-slim

WORKDIR /srv

# Instala dependências primeiro (cache de build mais eficiente)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copia o restante do projeto
COPY backend ./backend
COPY frontend ./frontend

WORKDIR /srv/backend

# O Railway injeta a variável PORT dinamicamente; expomos 8000 como padrão local
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
