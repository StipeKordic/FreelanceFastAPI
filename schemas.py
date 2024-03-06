import datetime
from typing import Optional, Union, List, Any
from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from humps import camelize


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


class ServiceRead(BaseModel):
    name: str
    id: int

    class Config:
        alias_generator = lambda x: camelize(x)
        populate_by_name = True


class UserReadForPost(BaseModel):
    email: str
    id: int

    class Config:
        alias_generator = lambda x: camelize(x)
        populate_by_name = True



'''
class ServiceOut(BaseModel):
    name: str
    description: str
    short_description: str

class ServiceOutWithNumber(BaseModel):
    Service: ServiceOut
    NumberOfPosts: int
'''

class ServiceUpdate(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    short_description: Union[str, None] = None


@form_body
class Post(BaseModel):
    description: str
    price: float
    service_id: int


class PostRead(BaseModel):
    description: str
    price: float
    service_id: int
    user_id: int
    image_path: str
    average_review: float
    number_of_reviews: int
    service: ServiceRead
    user: UserReadForPost

    class Config:
        alias_generator = lambda x: camelize(x)
        populate_by_name = True


class PostUpdate(BaseModel):
    description: Union[str, None] = None
    price: Union[float, None] = None


class QueryFilter(BaseModel):
    field: str
    operator: str
    value: Any

    def to_touple(self):
        return self.field, self.operator, self.value


class ServiceQuery(BaseModel):
    description: Optional[str] = None
    short_description: Optional[str] = None

    @property
    def get_operators(self):
        return {
            'description': 'like',
            'short_description': 'like'
        }

    @property
    def get_fields(self):
        return {
            'description': 'description',
            'short_description': 'short_description'
        }


class PostQuery(BaseModel):
    service_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    @property
    def get_operators(self):
        return {
            'service_id': 'eq',
            'min_price': 'ge',
            'max_price': 'le'
        }

    @property
    def get_fields(self):
        return {
            'service_id': 'service_id',
            'min_price': 'price',
            'max_price': 'price'
        }


class PostQueryByService(BaseModel):
    service_id: Optional[int] = None

    @property
    def get_operators(self):
        return {
            'service_id': 'eq'
        }

    @property
    def get_fields(self):
        return {
            'service_id': 'service_id'
        }


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


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserOut(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime.datetime
    image_path: str
    id: int

    class Config:
        alias_generator = lambda x: camelize(x)
        populate_by_name = True


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


class RoleOut(Role):
    id: int


class UserOutWithRole(BaseModel):
    User: UserOut
    Role: RoleOut


class Permission(BaseModel):
    permission_name: str


class PostOut(BaseModel):
    description: str
