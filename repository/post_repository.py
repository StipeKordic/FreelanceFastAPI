from typing import List
from sqlalchemy.orm import Session, selectinload
import models
from repository.base_repository import BaseRepository
from sqlalchemy import select, func

from schemas import QueryFilter


class PostRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def get_all_posts_filtered(self, session: Session, review: float, relation_attribute_name: List[str] = None, filters: List[QueryFilter] = None):
        posts = super().get_all(session, relation_attribute_name, filters)

        posts = [post for post in posts if post.average_review >= review]
        return posts

    def get_all_posts_of_user(self, session: Session, user_id: int):
        sql_stmt = select(self.class_model).where(self.class_model.user_id == user_id)
        result = session.execute(sql_stmt)
        return result.scalars().all()

    '''def get_review_info(self, session: Session, posts: List[models.Post]):

        # Calculate average rating and review count for each post
        for post in posts:
            post.review = (
                    session.query(func.avg(models.Review.review))
                    .filter(models.Review.post_id == post.id)
                    .scalar() or 0  # Handle the case where there are no reviews
            )

            post.number_of_reviews = (
                    session.query(func.count(models.Review.post_id))
                    .filter(models.Review.post_id == post.id)
                    .scalar() or 0  # Handle the case where there are no reviews
            )

        return posts

    def get_all_posts_filtered(self, session: Session, service_id: int):
        sql_stmt = select(self.class_model).where(self.class_model.service_id == service_id)
        result = session.execute(sql_stmt)

        return self.get_review_info(session, result.scalars().all())'''

'''
    def get_all_post_info(self):
        sql_stmt = select(self.class_model, func.count(models.Review.post_id), func.avg(
            models.Review.review), models.User.email, models.Service.name).join(
            models.User, models.Post.user_id == models.User.id).join(
            models.Service, models.Post.service_id == models.Service.id).join(
            models.Review, self.class_model.id == models.Review.post_id).group_by(
            self.class_model, models.User.email, models.Service.name)

        return sql_stmt
'''
