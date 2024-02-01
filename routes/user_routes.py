from typing import List
import sqlalchemy.exc
from fastapi import APIRouter, status, Depends, Response, File, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
from oauth2 import get_current_user, create_access_token
from schemas import User, UserUpdate, TokenData, UserOut, UserOutWithRole, ChangePassword
from PIL import Image
from io import BytesIO
import os
import secrets
import descriptions


user_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post("/signup", description=descriptions.create_user, response_model=UserOut)
async def create_user(user: User = Depends(User), file: UploadFile = File(None), db: Session = Depends(get_db)):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You didn't match the passwords.")

    user_in_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Email is already in use, please provide different one.")

    if file:
        if not file.content_type.startswith("image"):
            return {"error": "Invalid type"}

        image = Image.open(BytesIO(await file.read()))
        filepath = "/static/images/"
        filename = file.filename
        to_save = filepath + secrets.token_hex(10) + filename[-4::]
        image.save(os.path.join("static/images/", to_save[15::]))
    else:
        to_save = "/static/images/default.jpg"

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_data = user.model_dump()

    user_data.pop('confirm_password', None)

    new_user = models.User(**user_data, image_path=to_save)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_user_role = models.UserRole(user_id=new_user.id, role_id=3)
    db.add(new_user_role)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.get("/", description=descriptions.get_all_users, response_model=List[UserOutWithRole])
def get_all_users(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if "get_all_users" not in user.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")
    users = db.query(models.User, models.Role).select_from(models.User).join(models.UserRole).join(models.Role).all()

    users = list(map(lambda x: x._mapping, users))

    return users


@user_router.get("/{id}", description=descriptions.get_user_by_id, response_model=UserOutWithRole)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    try:
        user, role = db.query(models.User, models.Role).select_from(models.User).join(models.UserRole).join(models.Role).filter(models.User.id == id).first()
        response = {"User": user, "Role": role}
        print(utils.hash("user1"))
        return response
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with that id was not found")


@user_router.delete("/{id}", description=descriptions.delete_user)
def delete_user(id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    if "delete_user" not in user.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")

    user = db.query(models.User).filter(models.User.id == id)

    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.put("/image_update", description=descriptions.update_user_image, response_model=UserOut)
async def update_user_image(file: UploadFile = File(None), db: Session = Depends(get_db),
                            user_from_token: TokenData = Depends(get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == user_from_token.user_id)

    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if not file.content_type.startswith("image"):
        return {"error": "Invalid type"}
    image = Image.open(BytesIO(await file.read()))
    filepath = "/static/images/"
    filename = file.filename
    to_save = filepath + secrets.token_hex(10) + filename[-4::]
    image.save(os.path.join("static/images/", to_save[15::]))

    user.image_path = to_save

    db.commit()

    return user_query.first()


@user_router.put("/", description=descriptions.update_user)
async def update_user(updated_user: UserUpdate, db: Session = Depends(get_db),
                      user_from_token: TokenData = Depends(get_current_user)):

    user = db.query(models.User).filter(models.User.id == user_from_token.user_id).first()

    try:
        for attribute in updated_user:
            if attribute[1] is not None:
                setattr(user, attribute[0], attribute[1])
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already in use!")

    db.refresh(user)

    data = {"user_id": str(user.id), "first_name": user.first_name, "last_name": user.last_name,
            "role_id": str(user_from_token.role_id), "permissions": user_from_token.permissions}
    access_token = create_access_token(data)[0]
    refresh_token = create_access_token(data)[1]

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="User updated successfully",
        headers={"Authorization": f"Bearer {access_token}"},
    )


@user_router.put("/change_password")
def change_password(passwords: ChangePassword, db: Session = Depends(get_db),
                      user_from_token: TokenData = Depends(get_current_user)):

    user = db.query(models.User).filter(models.User.id == user_from_token.user_id).first()

    if (utils.verify(passwords.old_password, user.password)):
        hashed_password = utils.hash(passwords.new_password)
        user.password = hashed_password
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="Password changed successfully")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Passwords don't match")
