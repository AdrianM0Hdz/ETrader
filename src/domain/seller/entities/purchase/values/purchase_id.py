from dataclasses import dataclass
from typing import Tuple
from src.domain.common.value_object import ValueObject


class PurchaseId(ValueObject):
    def __init__(self, value: str):
        assert isinstance(value, str)
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])