import os
import secrets
from io import BytesIO
from typing import List
import asyncio
from PIL import Image

from schemas import QueryFilter
from services.result import Result
from sqlalchemy.orm import Session


class BaseController:
    def __init__(self, db: Session, repository):
        self.db = db
        self.default_repo = repository

    def get_many(self, query_params=None, relation_attribute_name: List[str] = None) -> Result:
        try:
            filters: List[QueryFilter] = self._pack_filters(query_params) if query_params else None
            items = self.default_repo.get_all(self.db, relation_attribute_name, filters)

            return Result.ok(items)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)

    def _pack_filters(self, query_params) -> List[QueryFilter]:
        filters = []
        for query_param in query_params:
            if query_param[1]:
                filters.append(QueryFilter(field=query_params.get_fields[query_param[0]],
                                           operator=query_params.get_operators[query_param[0]],
                                           value=query_param[1]))
        return filters

    def get_one(self, _id: int) -> Result:
        try:
            item = self.default_repo.get(self.db, _id)
            if not item:
                raise Exception("Not found")
            return Result.ok(item)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)

    async def create(self, item_in, file) -> Result:
        try:
            # print(item_in)
            to_save = await self.save_image(file)
            if to_save.success:  # This is not true if to_save=Result.fail("Invalid type")
                item = self.default_repo.create(self.db, item_in, to_save.item)  # Calling create method from either base_repository or user_repository
            else:
                return to_save
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    async def save_image(self, file=None) -> Result:
        if file:
            if not file.content_type.startswith("image"):  # If file type is not image return failed Result object
                return Result.fail("Invalid type")
            file_data = await file.read()
            image = Image.open(BytesIO(file_data))
            filepath = "/static/images/"
            filename = file.filename
            to_save = filepath + secrets.token_hex(10) + filename[-4::]
            image.save(os.path.join(filepath[1::], to_save[15::]))
            return Result.ok(to_save)  # If everything is good, return Result object with value being path to image
        else:
            return Result.fail("Image must be provided")  # If file was not sent, return Result object with value being path to default image (User profile default image)

    def update(self, item_in, item_id: int) -> Result:
        result: Result = self.get_one(item_id)
        if result.failure:
            return result
        try:
            item = self.default_repo.update(self.db, db_obj=result.value, obj_in=item_in)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    async def update_image(self, item_id: int, file) -> Result:
        if not file:
            return Result.fail("Image must be provided")
        result: Result = self.get_one(item_id)
        if result.failure:
            return result
        try:
            to_save = await self.save_image(file)
            item = self.default_repo.update_image(self.db, db_obj=result.value, image_path=to_save.item)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    def delete(self, item_id: int) -> Result:
        result: Result = self.get_one(item_id)
        if result.failure:
            return result
        try:
            item = self.default_repo.delete(self.db, db_obj=result.value)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)
