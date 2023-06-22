from typing import Tuple
from ...common.value_object import ValueObject


class Quantity(ValueObject):
    def __init__(self, value: int):
        assert isinstance(value, int)
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])
