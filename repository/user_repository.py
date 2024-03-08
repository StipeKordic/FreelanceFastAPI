from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def create(self, session, obj_in, image_path, password_hashed):
        obj_in_data = dict(obj_in)
        obj_in_data['image_path'] = image_path
        obj_in_data['password'] = password_hashed
        db_obj = self.class_model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def change_password(self, session: Session, new_password_hashed, db_obj):
        setattr(db_obj, 'password', new_password_hashed)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
