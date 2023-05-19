from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserPost(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserPost
    class Config:
        orm_mode = True

class Token(BaseModel):
    accees_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None