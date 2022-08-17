from logging import Handler
from sqlalchemy.orm.session import Session
from db.hashing import Hash
from fastapi import HTTPException, status

from db.models import User


def get_user_by_username(db: Session, username: str):
   user = db.query(User).filter(User.username==username).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
   return user
