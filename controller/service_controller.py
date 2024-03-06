from sqlalchemy.orm import Session
from controller.base_controller import BaseController
from models import Service
from repository.service_repository import ServiceRepository


class ServiceController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, ServiceRepository(Service))
