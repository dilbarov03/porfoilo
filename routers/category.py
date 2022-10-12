from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.models import Category
from .schemas import *
from db.database import get_db
from fastapi_pagination import Page, paginate
from typing import List

router = APIRouter(
   prefix = '/category',
   tags = ['category']
)

@router.get('/all', response_model=List[CategoryProjects])
def get_all(db: Session = Depends(get_db)):
   categories = db.query(Category).all()
   return categories

@router.post("/", response_model=CategoryDisplay)
def create_category(request: CategoryPost, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
   new_category = Category(
      title = request.title
   )

   db.add(new_category)
   db.commit()
   db.refresh(new_category)

   return new_category

@router.get("/{id}", response_model=CategoryProjects)
def get_category_projects(id: int, db: Session = Depends(get_db)):
   category = db.query(Category).filter(Category.id==id).first()
   if not category:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   return category

@router.patch("/{id}", response_model=CategoryDisplay)
def update_category(request: CategoryPost, id:int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
   category = db.query(Category).filter(Category.id==id).first()
   if not category:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   category.title = request.title

   db.commit()

   return category

@router.delete('/delete/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
   category = db.query(Category).filter(Category.id==id).first()
   if not category:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   if category.projects:
      for project in category.projects:
         db.delete(project)
   db.delete(category)
   db.commit()
   return 'Category with projects deleted successfully!'