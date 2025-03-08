from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2, utils, models, schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

#post. Usuario precisa passar suas credenciais. Envio de data em uma direção
#1o ve email e senha no banco depois cria token
@router.post("/login", response_model=schemas.Token)
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciais Invalidas")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciais Invalidas")
    #create token - o que quero que va no payload. Decidi que va o user id
    access_token = oauth2.create_acess_token(data = {"user_id": user.id})
    #return token
    return {"access_token":access_token, "token_type":"bearer"}
#o response model valida o retorno. Na função estava "access_tokens" no return enquanto que no pydantic token e deu erro