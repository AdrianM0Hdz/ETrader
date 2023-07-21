from dataclasses import dataclass

from typing import Tuple
from src.shared_kernel.domain.value_object import ValueObject
from ..enums import Cuerrency


class Price(ValueObject):
    def __init__(self, ammount: float, currency: Cuerrency):
        assert isinstance(ammount, float)
        assert isinstance(currency, Cuerrency)
        self.ammount = ammount
        self.currency = currency

    def get_equality_componets(self) -> Tuple:
        return tuple([self.ammount, self.currency])
