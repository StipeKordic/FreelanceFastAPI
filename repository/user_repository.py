from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def __str__(self):
        return "UserRepository"
