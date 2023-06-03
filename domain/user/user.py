from ..common.entity import Entity
from .user_id import UserId
from .username import Username


class User(Entity[UserId]):
    def __init__(self, id: UserId, username: Username):
        super().__init__(id)
        self._username = username

    @property
    def username(self) -> Username:
        return self._username

    @username.setter
    def username(self, new_username: Username):
        raise ValueError("username is not changable")
