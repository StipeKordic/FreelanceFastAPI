from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import descriptions
from schemas import Permission


permission_router = APIRouter(
    prefix='/permissions',
    tags=['permissions']
)


@permission_router.post("/", description=descriptions.create_permission)
def create_permission(permission: Permission, db: Session = Depends(get_db)):

    new_permission = models.Permission(**permission.model_dump())
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    new_permission_role = models.PermissionRole(permission_id=new_permission.id, role_id=2)
    db.add(new_permission_role)
    db.commit()
    db.refresh(new_permission)

    return new_permission


@permission_router.get("/", description=descriptions.get_all_permissions)
def get_all_permissions(db: Session = Depends(get_db)):
    permissions = db.query(models.Permission).all()
    return permissions


@permission_router.put("/roles/{permission_id}/{new_role_id}", description=descriptions.update_role_of_permission)
def update_role_of_permission(permission_id: int, new_role_id: int, db: Session = Depends(get_db)):

    permission_query = db.query(models.PermissionRole).filter(models.PermissionRole.permission_id == permission_id)
    permission = permission_query.first()
    permission.role_id = new_role_id
    db.commit()
    return {"Permission with role": permission_query.first()}


@permission_router.put("/{id}", description=descriptions.update_permission)
def update_permission(id: int, updated_permission: Permission, db: Session = Depends(get_db)):

    permission_query = db.query(models.Permission).filter(models.Permission.id == id)

    permission = permission_query.first()

    permission.permission_name = updated_permission.permission_name
    db.commit()

    return {"new_permission": permission_query.first()}
