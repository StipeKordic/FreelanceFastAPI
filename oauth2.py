from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import models
from schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_HOURS = os.getenv("REFRESH_TOKEN_EXPIRE_HOURS")


def create_access_token(data: dict, refresh_token: str = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if not refresh_token:
        refresh_token = create_refresh_token({"id": data["user_id"]})

    return [encoded_jwt, refresh_token]


def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=float(REFRESH_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def return_id(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("id")

    return user_id


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")
        first_name: str = payload.get("first_name")
        last_name: str = payload.get("last_name")
        role_id: str = payload.get("role_id")
        permissions = payload.get("permissions")

        if id is None:
            raise credentials_exception
        token_data = TokenData(user_id=id, last_name=last_name, first_name=first_name,
                               role_id=role_id, permissions=permissions)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    blacklisted = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == token).first()

    if blacklisted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not valid token")

    return verify_access_token(token, credentials_exception)
