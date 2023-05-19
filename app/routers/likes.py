from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from .. import oauth2, schemas, models, utils
from ..database import get_db


router = APIRouter(prefix = "/likes", tags = ["Likes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    
    post_exists = db.query(models.Post).filter(models.Post.id == like.post_id).first()    
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post does not exist")
    
    if like.direction == 1:
        
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "User has already liked the post")
        new_like = models.Like(post_id= like.post_id, user_id= current_user.id)
        db.add(new_like)
        db.commit()

        return {"message": "Post Liked"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User has not liked the post")
        
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post un-liked"}








