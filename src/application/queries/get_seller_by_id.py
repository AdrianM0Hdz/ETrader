from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ProductPurchaseData:
    id: str
    buyer_id: str
    quantity: int
    status: str


@dataclass(frozen=True)
class ProductPriceData:
    ammount: float
    currency: str


@dataclass(frozen=True)
class SellerProductData:
    id: str
    name: str
    description: str
    price: ProductPriceData
    purchases: Tuple[ProductPurchaseData]


@dataclass(frozen=True)
class SellerData:
    id: str
    name: str
    description: str
    products: Tuple[SellerProductData]


class GetSellerById(ABC):
    @abstractmethod
    def __call__(self, seller_id: str) -> SellerData:
        ...
