"""
Conexão com o banco de dados.

- Local/teste: SQLite (zero configuração), arquivo trilha_academica.db.
- Produção (Railway): a variável de ambiente DATABASE_URL é injetada
  automaticamente pelo plugin de PostgreSQL do Railway. Só precisamos
  normalizar o esquema, porque o Railway (como o Heroku) às vezes entrega
  a URL como "postgres://" e o SQLAlchemy exige "postgresql://".
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trilha_academica.db")

if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
