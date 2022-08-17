from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cloudinary 


SQLALCHEMY_DATABASE_URL = 'postgres://olbhfrcuqqpuik:73afafc5cbb346422a3e4d6a6b2b57c99dc15fc2be6d741f208e506cb7c14550@ec2-52-207-15-147.compute-1.amazonaws.com:5432/dlf9bu1oqt3b1'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})

#SQLALCHEMY_DATABASE_URL = "sqlite:///./mydatabase2.db"

cloudinary.config(
    cloud_name="progers",
    api_key="385595836119974",
    api_secret="VqTojQ56WOkvRsr2GFOByEDWgTk"
)

'''engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)'''


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
 
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()