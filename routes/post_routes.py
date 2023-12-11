from typing import Annotated, Union

from fastapi import APIRouter, status, Depends, Response, File, UploadFile, Header, Request
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import models
import descriptions
from schemas import Post, TokenData, PostUpdate
from oauth2 import get_current_user, oauth2_scheme
from PIL import Image
from io import BytesIO
import os
import secrets

post_router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@post_router.post("/", description=descriptions.create_post)
async def create_post(post: Post = Depends(Post), file: UploadFile = File(None), db: Session = Depends(get_db),
                      user: TokenData = Depends(get_current_user)):
    if file:
        if not file.content_type.startswith("image"):
            return {"error": "Invalid type"}
        image = Image.open(BytesIO(await file.read()))
        filepath = "/static/images/"
        filename = file.filename
        to_save = filepath + secrets.token_hex(10) + filename[-4::]
        image.save(os.path.join("static/images/", to_save[15::]))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image must be provided")

    new_post = models.Post(user_id=user.user_id, image_path=to_save, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@post_router.get("/", description=descriptions.get_all_posts)
def get_all_posts(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    posts = db.query(models.Post, func.avg(models.Review.review).label("Review"), func.count(models.Review.post_id).
                     label("Number of reviews")).join(models.Review, models.Post.id == models.Review.post_id,
                                                      isouter=True).group_by(models.Post).all()

    posts = list(map(lambda x: x._mapping, posts))
    return posts


@post_router.get("/service/{id}", description=descriptions.get_posts_by_service)
def get_posts_by_service(id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.service_id == id).all()
    return posts


@post_router.get("/filter/{id}", description=descriptions.get_posts_by_filter)
def get_posts_by_filter(id: int, min_price: float = 0, max_price: float = 999, review: float = 0,
                        db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    if review != 0:
        posts = (db.query(models.Post, func.avg(models.Review.review).label("Review")).join(models.Review, models.Post.id == models.Review.post_id, isouter=True)
                 .group_by(models.Post).having(func.avg(models.Review.review) >= review).filter(
            models.Post.service_id == id, models.Post.price >= min_price, models.Post.price <= max_price).all())
    else:
        posts = db.query(models.Post, func.avg(models.Review.review).label("Review")).join(models.Review, models.Post.id == models.Review.post_id,
                                       isouter=True).group_by(models.Post).filter(models.Post.service_id == id,
                                                                                  models.Post.price >= min_price,
                                                                                  models.Post.price <= max_price).all()
    posts = list(map(lambda x: x._mapping, posts))

    return posts


@post_router.get("/userPosts", description=descriptions.get_posts_of_logged_user)
def get_posts_of_logged_user(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == user.user_id).all()
    return posts


@post_router.get("/{id}", description=descriptions.get_post_by_id)
def get_post_by_id(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with that id not found")
    return {"Post": post}


@post_router.put("/image/{id}", description=descriptions.update_post_image)
async def update_post_image(id: int, file: UploadFile = File(None), db: Session = Depends(get_db),
                            user: TokenData = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    if not file.content_type.startswith("image"):
        return {"error": "Invalid type"}
    image = Image.open(BytesIO(await file.read()))
    filepath = "/static/images/"
    filename = file.filename
    to_save = filepath + secrets.token_hex(10) + filename[-4::]
    image.save(os.path.join("static/images/", to_save[15::]))

    post.image_path = to_save

    db.commit()

    return {"data": post_query.first()}


@post_router.put("/{id}", description=descriptions.update_post)
def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db),
                user: int = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with that id not found")

    if updated_post.description:
        post.description = updated_post.description

    if updated_post.price:
        post.price = updated_post.price

    db.commit()

    return {"data": post_query.first()}


@post_router.delete("/{id}", description=descriptions.delete_post)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@post_router.get("/example/")
def header_setter(request: Request):
    return request.headers
