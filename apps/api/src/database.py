from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Postgresql connection
#SQLALCHEMY_DATABASE_URL = os.getenv(
    #"DATABASE_URL",
    #"postgresql://postgres:Didrik2004.@localhost:5433/course_catalog"
#)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./courses.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'development-secret-key')


# Engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
