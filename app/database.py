from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLALCHEMY_DATABASE_URL = "mysql://root:Jahan%401024@localhost:3306/fastapi"
SQLALCHEMY_DATABASE_URL = f"mysql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
# # SQLALCHEMY_DATABASE_URL = "mysql://<user>:<password>@<postgresserver>/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,)

Base = declarative_base() 



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()