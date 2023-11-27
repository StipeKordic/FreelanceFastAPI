from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
import models
import descriptions
from oauth2 import get_current_user
from schemas import Role, TokenData

role_router = APIRouter(
    prefix='/roles',
    tags=['roles']
)


@role_router.post("/", description=descriptions.create_role)
def create_role(role: Role, db: Session = Depends(get_db)):

    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@role_router.get("/", description=descriptions.get_all_roles)
def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return roles


@role_router.put("/user/{user_id}/{new_role_id}", description=descriptions.update_role_of_user)
def update_role_of_user(user_id: int, new_role_id: int, db: Session = Depends(get_db),
                            user_from_token: TokenData = Depends(get_current_user)):

    if "update_role_of_user" not in user_from_token.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")

    user_query = db.query(models.UserRole).filter(models.UserRole.user_id == user_id)
    user = user_query.first()
    user.role_id = new_role_id
    db.commit()
    return {"User with role": user_query.first()}


@role_router.put("/{id}", description=descriptions.update_role)
def update_role(id: int, updated_role: Role, db: Session = Depends(get_db)):

    role_query = db.query(models.Role).filter(models.Role.id == id)

    role = role_query.first()

    role.role_name = updated_role.role_name
    db.commit()

    return {"new_role": role_query.first()}
