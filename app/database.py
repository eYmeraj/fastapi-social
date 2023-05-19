from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DATABAE_USERNAME = settings.database_username
DATABASE_PASSWORD = settings.database_password
DATABASE_HOSTNAME = settings.database_hostname
PORT_NUMBER = settings.database_port
DATABASE_NAME = settings.database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABAE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# import psycopg2
# from psycopg2.extras import RealDictCursor
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='psql', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('DB connection established')
#         break
#     except Exception as error:
#         print('Error connecting to DB')
#         print("Error", error)
#         time.sleep(2)