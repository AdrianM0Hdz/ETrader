from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BuyerPurchaseData:
    id: str
    seller_id: str
    product_id: str
    quantity: int
    status: str


@dataclass(frozen=True)
class BuyerData:
    id: str
    name: str
    purchases: Tuple[BuyerPurchaseData]


class GetBuyerById(ABC):
    @abstractmethod
    def __call__(self, user_id: str) -> BuyerData:
        ...
