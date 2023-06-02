from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

DATABAE_USERNAME = settings.database_username
DATABASE_PASSWORD = settings.database_password
DATABASE_HOSTNAME = settings.database_hostname
PORT_NUMBER = settings.database_port
DATABASE_NAME = settings.database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABAE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()