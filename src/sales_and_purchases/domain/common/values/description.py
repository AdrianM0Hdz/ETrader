from dataclasses import dataclass
from typing import Tuple
from src.shared_kernel.domain.value_object import ValueObject


@dataclass(frozen=True)
class DescriptionData:
    value: str


class Description(ValueObject):
    def __init__(self, value: str):
        assert isinstance(value, str)
        assert len(value) > 0
        assert len(value) <= 1000
        self.value = value

    def get_equality_componets(self) -> Tuple:
        return tuple([self.value])

    def get_data(self) -> DescriptionData:
        return DescriptionData(self.value)
