from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.exceptions import HTTPException
from db.hashing import Hash
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from db.models import About, User
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

@router.get("/about", response_model=schemas.AboutMe)
def get_about(db: Session = Depends(get_db)):
   return db.query(About).first()

@router.post("/about", response_model=schemas.AboutMe)
def create_about(request: schemas.AboutMeChange, db: Session = Depends(get_db), current_user: schemas.UserAuth = Depends(get_current_user)):
   new_about = About(
      title = request.title,
      text=request.text
   )

   db.add(new_about)
   db.commit()
   db.refresh(new_about)

   return new_about

@router.patch("/about", response_model=schemas.AboutMe)
def update_about(id:int, request: schemas.AboutMeChange, db: Session = Depends(get_db), 
              current_user: schemas.UserAuth = Depends(get_current_user)):
   
   about = db.query(About).filter(About.id==id).first()
   
   if not about:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   
   about.title = request.title
   about.text = request.text
   db.commit()

   return about