from typing import Annotated, Union, List

import sqlalchemy
from fastapi import APIRouter, status, Depends, Response, File, UploadFile, Header, Request
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

import utils
from database import get_db
import models
import descriptions
from schemas import Post, TokenData, PostUpdate, PostOut
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid type!")
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
def get_all_posts(db: Session = Depends(get_db), page: int = 1, user: int = Depends(get_current_user)):

    posts = (db.query(models.Post, func.avg(models.Review.review).label("Review"), func.count(models.Review.post_id).
                     label("Number of reviews"), models.User.email).select_from(models.Post).join(
        models.User, models.Post.user_id == models.User.id).join(models.Review, models.Post.id == models.Review.post_id
                                                                 , isouter=True).group_by(
                                                                                models.Post, models.User.email)
             .offset((page - 1) * 10).limit(10).all())

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries


@post_router.get("/service/{id}", description=descriptions.get_posts_by_service)
def get_posts_by_service(id: int, page: int = 1, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    posts = (db.query(models.Post, func.avg(models.Review.review).label("Review"), func.count(models.Review.post_id).
                     label("Number of reviews"), models.User.email).select_from(models.Post).join(
        models.User, models.Post.user_id == models.User.id).join(models.Review, models.Post.id == models.Review.post_id,
                                                      isouter=True).group_by(models.Post, models.User.email)
                                                    .filter(models.Post.service_id == id)
             .offset((page - 1) * 10).limit(10).all())

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries


@post_router.get("/filter", description=descriptions.get_posts_by_filter)
def get_posts_by_filter(service_id: int = 0, min_price: float = 0, max_price: float = 999
                        , review: float = 0, page: int = 1,
                        db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    basic_query = (db.query(models.Post, func.avg(models.Review.review).label("Review"),
                                      func.count(models.Review.post_id).label("Number of reviews"), models.User.email)
    .select_from(models.Post).join(models.User, models.Post.user_id == models.User.id)
    .join(models.Review, models.Post.id == models.Review.post_id, isouter=True)
                                    .group_by(models.Post, models.User.email).filter(
                                        models.Post.price >= min_price, models.Post.price <= max_price)
                                    )

    if service_id == 0 and review == 0:
        posts = basic_query.offset((page - 1) * 10).limit(10).all()
    elif service_id == 0 and review != 0:
        posts = basic_query.having(func.avg(models.Review.review) >= review).offset((page - 1) * 10).limit(10).all()
    elif service_id != 0 and review == 0:
        posts = basic_query.filter(models.Post.service_id == service_id).offset((page - 1) * 10).limit(10).all()
    else:
        posts = basic_query.having(func.avg(models.Review.review) >= review).filter(
            models.Post.service_id == service_id).offset((page - 1) * 10).limit(10).all()

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries


@post_router.get("/userPosts", description=descriptions.get_posts_of_logged_user)
def get_posts_of_logged_user(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    posts = (db.query(models.Post, func.avg(models.Review.review).label("Review"), func.count(models.Review.post_id).
                     label("Number of reviews")).join(models.Review, models.Post.id == models.Review.post_id,
                                                      isouter=True).group_by(models.Post)
                                                    .filter(models.Post.user_id == user.user_id).all())

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries


@post_router.get("/{id}", description=descriptions.get_post_by_id)
def get_post_by_id(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):


        post, review, num_reviews = (db.query(models.Post, func.avg(models.Review.review), func.count(models.Review.post_id))
                                     .join(models.Review).group_by(models.Post).filter(models.Post.id == id).first())
        response = {"Post": post, "Review": review, "Number of reviews": num_reviews}
        print(response)
        return response



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

    try:
        for attribute in updated_post:
            if attribute[1] is not None:
                setattr(user, attribute[0], attribute[1])
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already in use!")

    return {"data": post_query.first()}


@post_router.delete("/{id}", description=descriptions.delete_post)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
