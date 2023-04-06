from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # id: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title  1", "content": "content 1", "id": 1}, \
            {"title": "fav food", "content": "like pizza", "id": 2}]

@app.get("/")
def root():
    return {"message": "welcome to api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, ):
    post_dict = post.dict()
    post_dict['id'] = randint(0, 10e100)
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

@app.get("/posts/{id}")
def get_post(id: int, respoese: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                             detail=f"post with {id = } not found")
    return {"data": post}
