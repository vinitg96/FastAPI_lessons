# schema do pydantic valida só o que vai no body. O que vai no model_dump não preciso atualizar no modelo

from pydantic import BaseModel, ConfigDict, EmailStr, conint, Field
from typing import Optional, Annotated
from datetime import datetime




# pydantic -> create update post
#define a estrutura do meu request e response
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #owner_id: int

    model_config = ConfigDict(extra="forbid", from_attributes=True) #permite mapear campos que não estao no pydantic mas estao no banco

class UserBase(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid", from_attributes=True)


#E como from_attributes=True está no PostBase, ele pode mapear os atributos diretamente do objeto SQLAlchemy.

    #pydantic model po pradrao nao e um dicionario
    # class Config:
    #     orm_mode = True
    #from attribiutes atualizaç~pa do orm mode = true

    #rating: Optional[int] = None

# #todos os campos que eu quero que o usuario passe
# #para criar eu posso querer alguns campos e para editar outros diferentes
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

#     model_config = ConfigDict(extra="forbid")

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

#     model_config = ConfigDict(extra="forbid")


#o que eu quero que o usuario passe
class UserCreate(UserBase):
    pass

#o que volta para o ususario no request
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid", from_attributes=True)


###### usuario enviando para nos
#mimetiza o codigo comentado acima
#logica das rotas determinar o user_id. Nao precisa que usuario passe na body da request
class PostCreate(PostBase):
    #owner_id:int
    pass

class PostUpdate(PostBase):
    #title: Optional[str] = None
    # content: Optional[str] = None
    published: bool = True # usuario precisa determinar se foi publicado ou não


class PostResponse(PostBase):
    created_at: datetime
    id: int
    #owner_id: int
    #email: EmailStr
    owner: UserCreateResponse

class PostResponseVote(BaseModel):
    title: str
    id: int
    created_at: datetime
    owner_id: int
    email: EmailStr
    content: str
    published: bool
    n_votes: int
    model_config = ConfigDict(from_attributes=True)



#usuario precisa passar o token. COmo o usuario precisa passar algo, é bom definir um schema para isso
class Token(BaseModel):
    access_token: str
    token_type: str

# o que incuimos no tojken
class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    #dir: Annotated[int,conint(ge=0, le=1)]  # Annotated import restrições no tipo
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]



