from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models
import oauth2
import utils
from database import get_db
from schemas import TokenData
from oauth2 import get_current_user
import descriptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.post("/login")
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    user_role = db.query(models.UserRole).filter(models.UserRole.user_id == user.id).first()
    permissions = db.query(models.Permission).join(models.PermissionRole,
                                                   models.PermissionRole.permission_id == models.Permission.id,
                                                   isouter=True).filter(
        models.PermissionRole.role_id >= user_role.role_id).all()

    permissions_list = []
    for perm in permissions:
        permissions_list.append(perm.permission_name)

    data = {"user_id": str(user.id), "first_name": user.first_name, "last_name": user.last_name,
            "role_id": str(user_role.role_id), "permissions": permissions_list}

    tokens = oauth2.create_access_token(data)
    access_token = tokens[0]
    refresh_token = tokens[1]

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


@auth_router.post("/refresh_token", description=descriptions.create_new_access_token)
def create_new_access_token(token: str, db: Session = Depends(get_db)):
    user_id = oauth2.return_id(token)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user_role = db.query(models.UserRole).filter(models.UserRole.user_id == user.id).first()
    permissions = db.query(models.Permission).join(models.PermissionRole,
                                                   models.PermissionRole.permission_id == models.Permission.id,
                                                   isouter=True) \
        .filter(models.PermissionRole.role_id >= user_role.role_id).all()

    permissions_list = []
    for perm in permissions:
        permissions_list.append(perm.permission_name)

    data = {"user_id": str(user.id), "first_name": user.first_name, "last_name": user.last_name,
            "role_id": str(user_role.role_id), "permissions": permissions_list}

    access_token = oauth2.create_access_token(data, token)[0]

    return {"access_token": access_token, "refresh_token": token, "token_type": "Bearer"}


@auth_router.get("/logout")
def logout_user(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user),
                token: str = Depends(oauth2_scheme)):

    new_blacklist = models.TokenBlacklist(token=token)
    db.add(new_blacklist)
    db.commit()

    return {"message": "Logged out successfully"}
