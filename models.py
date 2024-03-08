from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(Text)
    short_description = Column(String(255), unique=True)
    image_path = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    posts = relationship('Post', back_populates="service")
    # posts = relationship('Post', back_populates="service", lazy="selectin")
    # This way above you can specify that every time you load all attributes (like for every service return
    # all of its posts instead of defining that in base_repository using relation_name)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    password = Column(String(255))
    image_path = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    posts = relationship('Post', back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(255), nullable=True)
    service = relationship('Service', back_populates="posts")
    user = relationship('User', back_populates="posts")
    reviews = relationship('Review')

    @property
    def average_review(self):
        if not self.reviews:
            return 0  # Handle the case where there are no reviews

        total_rating = sum(review.review for review in self.reviews)
        return total_rating / len(self.reviews)

    @property
    def number_of_reviews(self):
        if not self.reviews:
            return 0  # Handle the case where there are no reviews

        return len(self.reviews)


class Review(Base):
    __tablename__ = "reviews"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    review = Column(Float)


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, primary_key=True)


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    permission_name = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class PermissionRole(Base):
    __tablename__ = "permission_roles"
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, primary_key=True)


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    id = Column(Integer, primary_key=True)
    token = Column(String(255), unique=True)
    logout_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
