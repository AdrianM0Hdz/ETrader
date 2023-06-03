from typing import Tuple
from ..common.value_object import ValueObject


class Username(ValueObject):
    def __init__(self, value):
        assert isinstance(value, str)
        assert len(value) <= 50
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])
