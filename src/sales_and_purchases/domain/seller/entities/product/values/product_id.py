from typing import Tuple
from src.shared_kernel.domain.value_object import ValueObject


class ProductId(ValueObject):
    def __init__(self, value):
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])
