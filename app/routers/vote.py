from fastapi import Depends, status, HTTPException, APIRouter
from database import get_db
from sqlalchemy.orm import Session
import models
from oauth2 import get_current_user
import schemas

router = APIRouter(
     prefix="/vote",
     tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):

    #votar em um post que nao extiste
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post com o id {vote.post_id} nao existe")

        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        #verificar se vote ja existe para post especific
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} ja votou no post {vote.post_id}")
        
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return new_vote

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voto não existe")
        else:
            vote_query.delete(synchronize_session=False) ##para deletar posso chamar a aquery
            db.commit()
            return{"Voto Deletado"}
