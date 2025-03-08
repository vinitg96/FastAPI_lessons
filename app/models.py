from app.database import Base_ORM
from sqlalchemy import Column, String, Integer, Boolean,TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import Relationship

#nao referencia a classe na foreignkey
# se ja tiver a tabela com o nome posts sql alchemy nao faz nada
class Post(Base_ORM):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False )

    owner = Relationship("User")


class User(Base_ORM):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password =  Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base_ORM):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

    user = Relationship("User")
    post = Relationship("Post")