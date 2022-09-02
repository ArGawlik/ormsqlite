import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:DaftAcademy@127.0.0.1:5555/postgres"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine("sqlite:///northwind.db?check_same_thread=False&unicode_error=ignore")

# engine.raw_connection().connection.text_factory = lambda b: b.decode(errors="ignore", encoding="utf8")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
