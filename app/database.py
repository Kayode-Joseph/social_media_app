from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

#SQLALCHEMY_DATABASES_URL='postgresql://<username>:<password>@<server ip adress>/<databasename>'

SQLALCHEMY_DATABASES_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine=create_engine(SQLALCHEMY_DATABASES_URL)

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
