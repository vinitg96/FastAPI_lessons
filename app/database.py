# Interagindo com o banco via ORM

#https://www.youtube.com/watch?v=MHn1T2IZTLI&list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&index=45
#https://fastapi.tiangolo.com/tutorial/sql-databases/
#https://github.com/fastapi/full-stack-fastapi-template
# https://blog.stackademic.com/using-fastapi-with-sqlalchemy-5cd370473fe5


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


#SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#criar conexão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#mais facil de  criar outras instancias. Pode ser o session tb
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#será a classe base para os modelos SQLAlchemy.
Base_ORM = declarative_base()



# Cria uma sessão do banco de dados usando SessionLocal(), que provavelmente vem do SQLAlchemy.
# Usa yield db para "entregar" essa sessão para quem chamar a função.
# Após o uso da sessão, finally garante que ela será fechada, evitando vazamento de conexões.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()