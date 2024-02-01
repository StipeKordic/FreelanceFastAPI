import os
import secrets
from PIL import Image
from io import BytesIO
from fastapi import APIRouter, status, Depends, Response, File, UploadFile, Request
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import models
import descriptions
from schemas import Service, ServiceUpdate, TokenData
from oauth2 import get_current_user

service_router = APIRouter(
    prefix='/services',
    tags=['services']
)


@service_router.get("/", description=descriptions.get_all_services)
def get_all_services(db: Session = Depends(get_db)):
    services = db.query(models.Service, func.count(models.Post.service_id).label("Number of posts")).join(
        models.Post, models.Post.service_id == models.Service.id,isouter=True).group_by(models.Service).order_by(
        func.count(models.Post.service_id).desc()).all()

    services = list(map(lambda x: x._mapping, services))
    return services


@service_router.get("/{id}", description=descriptions.get_service_by_id)
def get_service_by_id(id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service with that id is not found")
    return {"Service": service}


@service_router.post("/", description=descriptions.create_service)
async def create_service(service: Service = Depends(Service), file: UploadFile = File(None),
                         db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    if "create_service" not in user.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")

    service_from_db_name = (db.query(models.Service.name).filter(models.Service.name == service.name))
    service_from_db_short_description = (db.query(models.Service.short_description)
                                         .filter(models.Service.short_description == service.short_description))

    if service_from_db_name.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service name already exists")
    elif service_from_db_short_description.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service short_description already exists")

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

    new_service = models.Service(name=service.name, description=service.description,
                                 short_description=service.short_description, image_path=to_save)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service
# This way name, description and short_description are sent as query parameters, so maybe it can be used here
# but probably not for creating user?

# @service_router.post("/s")
# async def create_service(name: str, description: str, short_description: str,
#                          file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if file:
#         if not file.content_type.startswith("image"):
#             return {"error": "Invalid type"}
#         image = Image.open(BytesIO(await file.read()))
#         filepath = "/static/images/"
#         filename = file.filename
#         to_save = filepath + secrets.token_hex(10) + filename[-4::]
#         image.save(os.path.join("static/images/", to_save[15::]))
#     else:
#         to_save = "/static/images/default.jpg"
#
#     new_service = models.Service(name=name, description=description,
#                                  short_description=short_description, image_path=to_save)
#     db.add(new_service)
#     db.commit()
#     db.refresh(new_service)
#
#     return {"Service": new_service}


@service_router.delete("/{id}", description=descriptions.delete_service)
def delete_service(id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):

    if "delete_service" not in user.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")

    service = db.query(models.Service).filter(models.Service.id == id)

    if service.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service does not exist")

    service.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@service_router.put("/image/{id}", description=descriptions.update_service_image)
async def update_service_image(id: int, file: UploadFile = File(None), db: Session = Depends(get_db),
                               user: TokenData = Depends(get_current_user)):

    if "update_service_image" not in user.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")

    service_query = db.query(models.Service).filter(models.Service.id == id)

    service = service_query.first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service does not exist")

    if not file.content_type.startswith("image"):
        return {"error": "Invalid type"}
    image = Image.open(BytesIO(await file.read()))
    filepath = "/static/images/"
    filename = file.filename
    to_save = filepath + secrets.token_hex(10) + filename[-4::]
    image.save(os.path.join("static/images/", to_save[15::]))

    service.image_path = to_save

    db.commit()

    return {"data": service_query.first()}


@service_router.put("/{id}", description=descriptions.update_service)
async def update_service(id: int, updated_service: ServiceUpdate, db: Session = Depends(get_db),
                         user: TokenData = Depends(get_current_user)):

    if "update_service" not in user.permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission!")

    service_query = db.query(models.Service).filter(models.Service.id == id)

    service = service_query.first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service does not exist")

    service_from_db_name = (db.query(models.Service.name).filter(models.Service.name == updated_service.name))
    service_from_db_short_description = (db.query(models.Service.short_description)
                                         .filter(models.Service.short_description == updated_service.short_description))

    if service_from_db_name.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service name already exists")
    elif service_from_db_short_description.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service short_description already exists")

    for attribute in updated_service:
        if attribute[1] is not None:
            setattr(service, attribute[0], attribute[1])

    db.commit()

    return {"data": service_query.first()}
