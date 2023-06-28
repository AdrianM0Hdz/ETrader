from dataclasses import dataclass

from typing import Tuple
from domain.common.value_object import ValueObject
from ..enums import Cuerrency


@dataclass(frozen=True)
class PriceData:
    ammount: float
    currency: Cuerrency


class Price(ValueObject):
    def __init__(self, ammount: float, currency: Cuerrency):
        assert isinstance(ammount, float)
        assert isinstance(currency, Cuerrency)
        self.ammount = ammount
        self.currency = currency

    def get_equality_componets(self) -> Tuple:
        return tuple([self.ammount, self.currency])

    def get_data(self) -> PriceData:
        return PriceData(self.ammount, self.currency)
