from typing import List, Optional

from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"] 

)

# @router.get("/", response_model= List[schemas.Post])
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, 
              skip: int = 0,
              search: Optional[str] = ''):

    posts = (db.query(models.Post, func.count(models.Like.post_id).label("likes"))
                    .join(models.Like, models.Like.post_id == models.Post.id, isouter= True)
                    .group_by(models.Post.id)
                    .filter(models.Post.title.contains(search))
                    .limit(limit)
                    .offset(skip)
                    .all())

    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = (db.query(models.Post, func.count(models.Like.post_id).label("likes"))
                        .join(models.Like, models.Like.post_id == models.Post.id, isouter= True)
                        .group_by(models.Post.id)
                        .filter(models.Post.id == id)
                        .first())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                             detail=f"post with {id = } not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                             detail=f"post with {id = } not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,\
                            detail= "You are not allowd to delete this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                             detail=f"post with {id = } not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,\
                            detail= "You are not allowd to delete this post")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
