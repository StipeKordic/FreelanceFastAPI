from sqlalchemy.orm import Session
from controller.base_controller import BaseController
from models import User
from repository.user_repository import UserRepository
from services.result import Result
from utils import confirm_password, verify_password, hash_password


class UserController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, UserRepository(User))

    async def create(self, item_in, file=None) -> Result:
        try:
            password_hashed = hash_password(item_in.password)
            to_save = await super().save_image(file)
            if to_save.success:  # This is not true if to_save=Result.fail("Invalid type")
                item = self.default_repo.create(self.db, item_in, to_save.item, password_hashed)  # Calling create method from either base_repository or user_repository
            else:
                item = self.default_repo.create(self.db, item_in, "/static/images/default.jpg", password_hashed)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    async def update_image(self, item_id: int, file=None) -> Result:
        """
        Method for changing profile image of user. To set users profile picture to default
         one (or to remove image) do not send a file.
        """
        result: Result = super().get_one(item_id)
        if result.failure:
            return result
        try:
            to_save = await super().save_image(file)
            item = self.default_repo.update_image(self.db, db_obj=result.value, image_path=to_save.item)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    def change_password(self, passwords, user_id) -> Result:
        try:
            result: Result = super().get_one(user_id)
            if not verify_password(passwords.old_password, result.value.password):
                return Result.fail("Incorrect password")
            new_password_hashed = hash_password(passwords.new_password)
            item = self.default_repo.change_password(self.db, new_password_hashed, result.value)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)
