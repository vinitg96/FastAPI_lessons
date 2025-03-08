
#postgres container b7c908a93029
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from fastapi import FastAPI
from database import engine
import models #database
from config import settings
from fastapi.middleware.cors import CORSMiddleware


from app.routers import post, user, auth, vote

# Ele pega todos os modelos ORM que herdam de Base e cria as tabelas correspondentes no PostgreSQL.
# Se a tabela já existir, não faz nada.
#com o alembic não precisa desse comando
#models.Base_ORM.metadata.create_all(bind = engine)

app = FastAPI()
#permitir especificaos headers, https, e do´minios
#origins = ["https://www.google.com"]
origins = ["*"] #não recomendado

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router) #direciona para router e ve se path da match
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/", tags=["home"])
def home():
    return "Hello World"

