from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
import descriptions
from schemas import Review, TokenData
from oauth2 import get_current_user


review_router = APIRouter(
    prefix='/review',
    tags=['review']
)


@review_router.post("/", description=descriptions.review_post)
def review_post(review: Review, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    review_query = db.query(models.Review).filter(
        models.Review.post_id == review.post_id, models.Review.user_id == user.user_id)
    found_review = review_query.first()
    if not found_review:
        new_review = models.Review(user_id=user.user_id, **review.model_dump())
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        return new_review
    else:
        review_query.update(review.model_dump(), synchronize_session=False)
        db.commit()

        return review


@review_router.get("/{id}", description=descriptions.get_review_of_post)
def get_review_of_post(id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    total_sum_reviews = db.query(func.sum(models.Review.review)).filter(models.Review.post_id == id).first()
    num_reviews = db.query(func.count(models.Review.post_id)).filter(models.Review.post_id == id).first()

    return {"review": total_sum_reviews[0]/num_reviews[0], "Number of reviews": num_reviews[0]}
