from typing import List
from models.user import User
from controllers.user_db import UserDB


class UserController:
    def __init__(self, user_crud: UserDB):
        self.user_crud = user_crud

    def create_user(self, name: str) -> int:
        return self.user_crud.create(name)

    def list_users(self) -> List[User]:
        return self.user_crud.read_all()

    def get_user(self, user_id: int) -> User | None:
        return self.user_crud.read_by_id(user_id)