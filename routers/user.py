from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from db.hashing import Hash
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from db.models import User
from routers import schemas
import cloudinary
import cloudinary.uploader

router = APIRouter(
   tags=['user']
)

@router.get("/", response_model=schemas.UserDisplay)
def get_user(db: Session = Depends(get_db), current_user: schemas.UserAuth = Depends(get_current_user)):
   user = db.query(User).filter(User.id==current_user.id).first()
   return user

@router.post("/user", response_model=schemas.UserDisplay)
def create_profile(request: schemas.UserPost, db: Session = Depends(get_db)):
   new_user = User(
      username = request.username,
      password = Hash.bcrypt(request.password),
      avatar_url = request.avatar_url
   )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return new_user
   
@router.post('/user/image')
def upload_image(file: UploadFile = File(...)):
   result = cloudinary.uploader.upload(file.file)
   url = result.get("url")

   return {'path': url}

@router.patch("/update", response_model=schemas.UserDisplay)
def update_user(request: schemas.UserPost, db: Session = Depends(get_db), current_user: schemas.UserAuth = Depends(get_current_user)):
   user = db.query(User).filter(User.username==current_user.username).first()
   if request.username: 
      user.username = request.username
   if request.password:
      user.password = Hash.bcrypt(request.password)
   if request.avatar_url:
      user.avatar_url = request.avatar_url

   db.commit()
   return user
   
@router.delete("/delete")
def delete(db: Session = Depends(get_db), current_user: schemas.UserAuth = Depends(get_current_user)):
   user = db.query(User).filter(User.username==current_user.username).first()
   db.delete(user)
   db.commit()

   return "User deleted successfully"