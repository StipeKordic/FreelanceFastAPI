import math
from typing import List

import sqlalchemy
from fastapi import APIRouter, status, Depends, Response, File, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import models
import descriptions
from schemas import Post, TokenData, PostUpdate, PostRead, PostQuery, PostQueryByService
from oauth2 import get_current_user
from PIL import Image
from io import BytesIO
import os
import secrets
from controller.post_controller import PostController
from services.result import Result

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


@post_router.get("/", response_model=List[PostRead])
def get_all_posts(db: Session = Depends(get_db)):
    cont = PostController(db)
    result: Result = cont.get_many()
    return result.items


'''@post_router.get("/", description=descriptions.get_all_posts)
def get_all_posts(db: Session = Depends(get_db), page: int = 1, user: int = Depends(get_current_user)):

    posts = (db.query(models.Post, func.avg(models.Review.review).label("Review"),
                      func.count(models.Review.post_id).label("Number of reviews"), models.User.email, models.Service.name)
             .select_from(models.Post).join(models.User, models.Post.user_id == models.User.id).join(models.Service, models.Post.service_id == models.Service.id)
             .join(models.Review, models.Post.id == models.Review.post_id, isouter=True)
             .group_by(models.Post, models.User.email, models.Service.name).offset((page - 1) * 12).limit(12).all())

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries
'''

@post_router.get("/service", description=descriptions.get_posts_by_service, response_model=List[PostRead])
def get_posts_by_service(query: PostQueryByService = Depends(), db: Session = Depends(get_db),
                         user: TokenData = Depends(get_current_user)):
    cont = PostController(db)
    result: Result = cont.get_many(query_params=query)
    return result.items


@post_router.get("/filter", response_model=List[PostRead])
def get_posts_by_filter(review: float, db: Session = Depends(get_db), query: PostQuery = Depends(), user: TokenData = Depends(get_current_user)):

    cont = PostController(db)
    result: Result = cont.filter_posts_by_review(review=review, query_params=query)
    return result.items
'''
@post_router.get("/filter", description=descriptions.get_posts_by_filter)
def get_posts_by_filter(service_id: int = 0, min_price: int = 0, max_price: int = 999,
                        review: float = 0, page: int = 1,
                        db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    basic_query = (db.query(models.Post, func.avg(models.Review.review).label("Review"),
                            func.count(models.Review.post_id).label("Number of reviews"), models.User.email, models.Service.name)
                   .select_from(models.Post).join(models.User, models.Post.user_id == models.User.id).join(models.Service, models.Post.service_id == models.Service.id)
                   .join(models.Review, models.Post.id == models.Review.post_id, isouter=True)
                   .group_by(models.Post, models.User.email, models.Service.name)
                   .filter(models.Post.price >= min_price, models.Post.price <= max_price))

    if service_id == 0 and review == 0:
        posts = basic_query.offset((page - 1) * 12).limit(12).all()
    elif service_id == 0 and review != 0:
        posts = basic_query.having(func.avg(models.Review.review) >= review).offset((page - 1) * 12).limit(12).all()
    elif service_id != 0 and review == 0:
        posts = basic_query.filter(models.Post.service_id == service_id).offset((page - 1) * 12).limit(12).all()
    else:
        posts = basic_query.having(func.avg(models.Review.review) >= review).filter(
            models.Post.service_id == service_id).offset((page - 1) * 12).limit(12).all()

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries
'''
'''
@post_router.get("/userPosts", description=descriptions.get_posts_of_logged_user)
def get_posts_of_logged_user(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    posts = (db.query(models.Post, func.avg(models.Review.review).label("Review"), func.count(models.Review.post_id)
                      .label("Number of reviews"), models.User.email, models.Service.name).select_from(models.Post)
             .join(models.User, models.Post.user_id == models.User.id).join(models.Service, models.Post.service_id == models.Service.id)
             .join(models.Review, models.Post.id == models.Review.post_id, isouter=True)
             .group_by(models.Post, models.User.email, models.Service.name).filter(models.Post.user_id == user.user_id).all())

    posts = list(map(lambda x: x._mapping, posts))
    list_of_dictionaries = [dict(post) for post in posts]
    for post in list_of_dictionaries:
        if not post["Review"]:
            post["Review"] = 0

    return list_of_dictionaries'''


@post_router.get("/userPosts", response_model=List[PostRead])
def get_posts_of_logged_user(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    cont = PostController(db)
    result: Result = cont.get_many_posts_of_user(user.user_id)
    return result.items


@post_router.get("/{post_id}", description=descriptions.get_post_by_id)
def get_post_by_id(post_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):

    try:
        post, review, num_reviews, email, service = (db.query(models.Post, func.avg(models.Review.review),
                                                     func.count(models.Review.post_id), models.User.email, models.Service.name)
                                            .select_from(models.Post)
                                            .join(models.User, models.Post.user_id == models.User.id)
                                            .join(models.Service, models.Post.service_id == models.Service.id)
                                            .join(models.Review, models.Post.id == models.Review.post_id, isouter=True)
                                            .group_by(models.Post, models.User.email, models.Service.name)
                                            .filter(models.Post.id == post_id).first())

    except TypeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")
    response = {"Post": post, "Review": review, "Number of reviews": num_reviews, "User": email, "Service": service}
    return response


@post_router.put("/image/{post_id}", response_model=PostRead)
async def update_post_image(post_id: int, file: UploadFile = File(None), db: Session = Depends(get_db),
                            user: TokenData = Depends(get_current_user)):
    cont = PostController(db)
    result: Result = await cont.update_image(post_id, file)
    return result.item

'''
@post_router.put("/image/{post_id}", description=descriptions.update_post_image)
async def update_post_image(post_id: int, file: UploadFile = File(None), db: Session = Depends(get_db),
                            user: TokenData = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    if post.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You can only update your posts!")

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
'''


@post_router.put("/{post_id}", description=descriptions.update_post)
def update_post(post_id: int, updated_post: PostUpdate, db: Session = Depends(get_db),
                user: int = Depends(get_current_user)):

    cont = PostController(db)
    result: Result = cont.update(updated_post, post_id)
    return result.item


'''
@post_router.put("/{post_id}", description=descriptions.update_post)
def update_post(post_id: int, updated_post: PostUpdate, db: Session = Depends(get_db),
                user: int = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with that id not found")

    if post.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You can only update your posts!")

    for attribute in updated_post:
        if attribute[1] is not None:
            setattr(post, attribute[0], attribute[1])
    db.commit()


    return {"data": post_query.first()}
'''

@post_router.delete("/{post_id}", description=descriptions.delete_post)
def delete_post(post_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    print(post_query.first().user_id, user.user_id, user.role_id)
    if (post_query.first().user_id != user.user_id) and (user.role_id == "3"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You can only update your posts!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
