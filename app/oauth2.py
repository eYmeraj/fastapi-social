from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models
# SECTER_KEY
# ALGORITHM 
# expiration time of token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')


SECRET_KEY = "d0f51a97e7b12a0f2d00b3cee0b8459116ba416c7031d0f78f9ed40485577660"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTER = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTER)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verifyt_access_token(token: str, crediantials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise crediantials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise crediantials_exception

    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail = f"could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verifyt_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
