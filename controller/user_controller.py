from sqlalchemy.orm import Session
from controller.base_controller import BaseController
from models import User
from repository.user_repository import UserRepository
from services.result import Result


class UserController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, UserRepository(User))
