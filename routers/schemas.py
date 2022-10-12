from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserPost(BaseModel):
   username: str
   password: str
   avatar_url: str


class UserDisplay(BaseModel):
   username: str
   avatar_url : str
   class Config():
      orm_mode = True

class UserAuth(BaseModel):
   id: int
   username: str

class CategoryPost(BaseModel):
   title: str

class CategoryDisplay(BaseModel):
   id: int
   title: str

   class Config():
      orm_mode = True

class ProjectPost(BaseModel):
   title: str
   text: str
   image_url: str
   demo_link: Optional[str]
   github_link: Optional[str]
   category_id: int

class ProjectUpdate(BaseModel):
   title: Optional[str]
   text: Optional[str]
   image_url: Optional[str]
   demo_link: Optional[str]
   github_link: Optional[str]
   category_id: Optional[int]

class ProjectDisplay(BaseModel):
   id: int
   title: str
   text: str
   image_url: str
   demo_link: Optional[str]
   github_link: Optional[str]
   timestamp: datetime
   category_id: int
   category: CategoryDisplay

   class Config():
      orm_mode = True

class CategoryProjects(BaseModel):
   id: int
   title: str
   projects: List[ProjectDisplay]

   class Config():
      orm_mode = True


class AboutMe(BaseModel):
   id: int
   title: str
   text: str
   
   class Config():
      orm_mode = True
   
class AboutMeChange(BaseModel):
   title: str
   text: str