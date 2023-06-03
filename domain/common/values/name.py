from typing import Tuple
from ..value_object import ValueObject


class Name(ValueObject):
    def __init__(self, value: str):
        assert isinstance(value, str)
        assert len(value) > 0
        assert len(value) <= 50
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple(list(self.value))
