from dataclasses import dataclass
from typing import Tuple
from ..value_object import ValueObject


@dataclass(frozen=True)
class NameData:
    value: str


class Name(ValueObject):
    def __init__(self, value: str):
        assert isinstance(value, str)
        assert len(value) > 0
        assert len(value) <= 50
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple(list(self.value))

    def get_data(self) -> NameData:
        return NameData(self.value)
