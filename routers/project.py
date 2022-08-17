from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.models import Project
from .schemas import *
from db.database import get_db
import cloudinary
import cloudinary.uploader
from fastapi_pagination import Page, paginate


router = APIRouter(
   prefix = '/project',
   tags = ['project']
)


@router.get('/all', response_model=List[ProjectDisplay])
def get_all(db: Session = Depends(get_db)):
   projects = db.query(Project).all()
   return projects

@router.get('/{id}', response_model=ProjectDisplay)
def get_project(id: int, db: Session = Depends(get_db)):
   project = db.query(Project).filter(Project.id==id).first()
   if not project:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")
   return project     


@router.patch('/{id}', response_model=ProjectDisplay)
def update_post(request: ProjectUpdate, id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
   project = db.query(Project).filter(Project.id==id).first()
   if not project:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")
   
   if request.title:
      project.title = request.title
   
   if request.title:
      project.text = request.text
   
   if request.image_url:
      project.image_url = request.image_url

   if request.demo_link:
      project.demo_link = request.demo_link

   if request.github_link:
      project.github_link = request.github_link

   if request.category_id:
      project.category_id = request.category_id

   db.commit() #save

   return project

@router.post('/', response_model=ProjectDisplay)
def create(request: ProjectPost, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
   
   new_project = Project(
      title = request.title,
      text = request.text,
      image_url = request.image_url,
      demo_link = request.demo_link,
      github_link = request.github_link, 
      timestamp = datetime.now(),
      category_id = request.category_id
   )
   db.add(new_project)
   db.commit()
   db.refresh(new_project)

   return new_project

@router.post('/image')
def upload_image(file: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
   result = cloudinary.uploader.upload(file.file)
   url = result.get("url")

   return {'path': url}


@router.delete('/delete/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
   project = db.query(Project).filter(Project.id==id).first()
   if not project:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")
   db.delete(project)
   db.commit()
   return 'Project deleted successfully!'