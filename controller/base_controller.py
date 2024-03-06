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

    async def create(self, item_in, file=None) -> Result:
        try:
            # print(item_in)
            if file or str(self.default_repo) == "UserRepository":
                if file:
                    if not file.content_type.startswith("image"):
                        return Result.fail("Invalid type")
                    file_data = await file.read()
                    image = Image.open(BytesIO(file_data))
                    filepath = "/static/images/"
                    filename = file.filename
                    to_save = filepath + secrets.token_hex(10) + filename[-4::]
                    image.save(os.path.join("static/images/", to_save[15::]))
                else:
                    to_save = "/static/images/" + "default.jpg"
            else:
                return Result.fail("Image must be provided")
            item = self.default_repo.create(self.db, item_in, to_save)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    def update(self, item_in, item_id: int) -> Result:
        result: Result = self.get_one(item_id)
        if result.failure:
            return result
        try:
            item = self.default_repo.update(self.db, db_obj=result.value, obj_in=item_in)
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
