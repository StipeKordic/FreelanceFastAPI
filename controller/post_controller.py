from typing import List

from sqlalchemy.orm import Session
from controller.base_controller import BaseController
from models import Post
from repository.post_repository import PostRepository
from schemas import QueryFilter
from services.result import Result


class PostController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, PostRepository(Post))

    def filter_posts_by_review(self, query_params, review: float = 0, relation_attribute_name: List[str] = None) -> Result:
        try:
            filters: List[QueryFilter] = self._pack_filters(query_params)
            items = self.default_repo.get_all_posts_filtered(self.db, review, relation_attribute_name, filters)
            return Result.ok(items)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)

    def get_many_posts_of_user(self, user_id: int) -> Result:
        try:
            items = self.default_repo.get_all_posts_of_user(self.db, user_id)
            return Result.ok(items)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)


''' 
    def get_many_posts_filtered(self, service_id: int) -> Result:
        try:
            items = self.default_repo.get_all_posts_filtered(self.db, service_id)
            return Result.ok(items)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)'''
