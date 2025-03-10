from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..utils import hahsing_password


router = APIRouter(
     prefix="/users",
     tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):


    user.password = hahsing_password(user.password)


    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[schemas.UserCreateResponse])
def get_all_users(db: Session = Depends(get_db)):
        users = db.query(models.User).all()
        return users

@router.get("/{id}", response_model=schemas.UserCreateResponse) 
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    return user