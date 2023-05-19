import time
from typing import Optional, List

from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='psql', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DB connection established')
        break
    except Exception as error:
        print('Error connecting to DB')
        print("Error", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "welcome to api"}
