from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import ARRAY, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.ext.mutable import MutableList


class User(Base):
   __tablename__ = "user"
   id = Column(Integer, primary_key=True, index=True)
   username = Column(String, unique=True)
   password = Column(String)
   avatar_url = Column(String, default="")
   
class Category(Base):
   __tablename__ = "category"
   id = Column(Integer, primary_key=True, index=True)
   title = Column(String)
   projects = relationship("Project", back_populates="category")

class Project(Base):
   __tablename__ = "projects"
   id = Column(Integer, primary_key=True, index=True) 
   title = Column(String)
   text = Column(String)
   image_url = Column(String)
   demo_link = Column(String, nullable=True)
   github_link = Column(String, nullable=True)
   timestamp = Column(DateTime)
   category_id = Column(Integer, ForeignKey('category.id'))
   
   category = relationship("Category", back_populates="projects")

class About(Base):
   __tablename__ = "about"
   id = Column(Integer, primary_key=True, index=True)
   title = Column(String)
   text = Column(String)