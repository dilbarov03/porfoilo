from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.sql.functions import mode
from db import models
from db.database import engine
from routers import project, user, category
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(category.router)
app.include_router(project.router)

app.include_router(authentication.router)

@app.get("/")
def root():
   return 'hello oktamjon'

origins = [
   'http://localhost:3000'
]

app.add_middleware(
   CORSMiddleware,
   #allow_origins=origins,
   allow_origins=['*'],
   allow_credentials=True,
   allow_methods=['*'],
   allow_headers=['*']
)

models.Base.metadata.create_all(engine)

add_pagination(app)