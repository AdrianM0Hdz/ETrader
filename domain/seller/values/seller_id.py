from typing import Tuple
from ...common.value_object import ValueObject


class SellerId(ValueObject):
    def __init__(self, value):
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])
