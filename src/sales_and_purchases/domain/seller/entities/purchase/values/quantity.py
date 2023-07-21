from dataclasses import dataclass
from typing import Tuple
from src.shared_kernel.domain.value_object import ValueObject


class Quantity(ValueObject):
    def __init__(self, value: int):
        assert isinstance(value, int)
        assert value > 0
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])
