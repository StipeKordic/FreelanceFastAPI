from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repository.base_repository import BaseRepository


class ServiceRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
