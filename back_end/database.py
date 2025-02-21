from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import getpass

#host = "localhost"
#database=input("Informe o DB: ")
#user=input("Usuario: ")
#password=input("Senha: ")

user = input("USER: ")
password = getpass.getpass("PASSWORD: ")
#user = "teste"
#password = "123"
database = "pdsi"
host = "localhost"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mangue@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
