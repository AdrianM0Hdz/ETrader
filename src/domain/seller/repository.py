from abc import ABC, abstractmethod

from src.domain.common.repository import Repository
from . import Seller
from .values import SellerId


class SellerRepository(Repository, ABC):
    @abstractmethod
    def add(self, item: Seller):
        ...

    @abstractmethod
    def get(self, id: SellerId) -> Seller:
        ...

    @abstractmethod
    def commit(self, item: Seller):
        ...

    @abstractmethod
    def delete(self, item: Seller):
        ...
