from typing import Tuple
from hashlib import sha512
from src.shared_kernel.domain.value_object import ValueObject


class PasswordHash(ValueObject):
    def __init__(self, raw_password: str):
        assert isinstance(raw_password, str)
        self.value = sha512(bytes(raw_password, "utf-8")).hexdigest()

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])
