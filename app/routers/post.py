from fastapi import Depends, status, HTTPException, APIRouter
import models, schemas
from database import get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from sqlalchemy.sql import func
from typing import List, Optional
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

#{URL}}posts?limit=2&skip=3
#{{URL}}posts?limit=100&search=meu%20dia
#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model= List[schemas.PostResponseVote])
#@router.get("/")
def get_posts(db: Session = Depends(get_db), limit:int = 100, skip:int = 0, search:Optional[str] = ""):
    #print(limit)
    #posts = db.query(models.Post).all()
    #query parameters
    #print(search)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #sql alchemy retorna uma lista de tuplas [(models.Post, n_votes)]
    #** desempacota novo dicionario, o que vem depois é apendado
    # results = db\
    #     .query(models.Post, func.count(models.Vote.user_id).label("n_votes"))\
    #     .join(target=models.Vote, onclause=models.Post.id==models.Vote.post_id, isouter=True)\
    #     .options(joinedload(models.Post.owner))\
    #     .group_by(models.Post.id)\
    #     .all()

    query = text(""" 
    WITH posts_votes AS (
        SELECT posts.*, COUNT(votes.user_id) AS n_votes 
        FROM posts
        LEFT JOIN votes ON posts.id = votes.post_id
        WHERE posts.title ILIKE :search  -- Aplica filtro pelo título
        GROUP BY posts.id
    )
    SELECT posts_votes.*, users.email 
    FROM posts_votes
    LEFT JOIN users ON posts_votes.owner_id = users.id
    LIMIT :limit OFFSET :skip  -- Aplica paginação
    """)
    results = db.execute(query, {"search": f"%{search}%", "limit": limit, "skip": skip}).fetchall()
    print(results)
    #results = db.execute(query).fetchall()
    colunas = ["id", "title", "content", "owner_id", "published", "created_at", "n_votes", "email"]
    results = [dict(zip(colunas, result)) for result in results]

    print(results)
    # Retorna uma lista de tuplas ((models.Post, int)) → FastAPI não sabe como lidar com isso automaticamente.
    #print(results) mostrar a query sem o .all()
    #return [{**post.__dict__, "n_votes": n_votes} for post, n_votes in results]

    return results

    #return posts
    #return posts
    #return dict(results[0]




#retornar apenas os posts de pessoas logadas
@router.get("/logged", response_model=List[schemas.PostResponse])
def get_logged_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts
                     


@router.get("/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    result = db.execute(text(""" SELECT * FROM posts ORDER BY id DESC LIMIT 1 """))
    last_post = dict(result.fetchone()._mapping)
    return last_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id:int, db: Session = Depends(get_db)):

    post_find = db.query(models.Post).filter(models.Post.id == id).first()

    print(post_find.__dict__)
    
    if not post_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post_find

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostUpdate, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)): 
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    elif query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não autorizada")
    
    query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return query.first()


#2a depednccia força a pessoa a estar logada para conseguir criar um post
# antes trazia so o id -> def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), user_id:int  = Depends(oauth2.get_current_user)):
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user:models.User  = Depends(oauth2.get_current_user)):

    
    #print(current_user.email)
    #new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    new_post = models.Post(**post.model_dump())
    new_post.owner_id = current_user.id
    #new_post.email = current_user.email
    #print(new_post.owner_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  

    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    print(current_user)

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post com o ID {id} não encontrado")
    elif deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não permitida")
    else:
        deleted_post.delete(synchronize_session=False)
        db.commit()
    


