from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def create(self, session, obj_in, image_path):
        # image_path is either path to real image or path to default image but for user both paths are ok,
        # so it is saved
        obj_in_data = dict(obj_in)
        obj_in_data['image_path'] = image_path
        db_obj = self.class_model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
