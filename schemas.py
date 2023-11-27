import datetime
from typing import Optional, Union, List
from pydantic import BaseModel, EmailStr
from fastapi import Form


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class Service(BaseModel):
    name: str
    description: str
    short_description: str


class ServiceUpdate(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    short_description: Union[str, None] = None


@form_body
class Post(BaseModel):
    description: str
    price: float
    service_id: int


class PostUpdate(BaseModel):
    description: Union[str, None] = None
    price: Union[float, None] = None


@form_body
class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserUpdate(BaseModel):
    email: Union[EmailStr, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    old_password: Union[str, None] = None
    new_password: Union[str, None] = None


class UserOut(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime.datetime
    image_path: str


class TokenData(BaseModel):
    user_id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: Optional[str]
    permissions: List[str]


class Review(BaseModel):
    post_id: int
    review: float


class Role(BaseModel):
    role_name: str


class Permission(BaseModel):
    permission_name: str
