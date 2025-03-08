import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
import models
from config import settings

#endpoint do login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_acess_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)

    #current time and + 30 minutes
    return encoded_jwt

def verify_access_token(token: str, credetntials_exceptions):

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id:str = payload.get("user_id")

        if id is None:
            raise credetntials_exceptions
        #valida se bate com token schema
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credetntials_exceptions
    
    return token_data

#extrair id do token automaticamente e retornar o susuario
#passar isso como depednencia toda vez que quero um endpoint que seja necessario estar logado. 
#por exemplo, no post


####### OLD SEM FECTHAR DO BANCO O USUARIO
# def get_current_user(token:str = Depends(oauth2_scheme)):
#     credentials_exceptions = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail=f"Could not validate credentials",
#         headers={"WWW-Authenticate":"Bearer"})
    
#     return verify_access_token(token, credentials_exceptions)


def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exceptions)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
