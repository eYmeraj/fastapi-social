from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth, likes

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)

@app.get("/")
def root():
    return {"message": "welcome to api"}
