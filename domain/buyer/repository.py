from abc import ABC, abstractmethod

from ..common.repository import Repository

from .buyer import Buyer
from .values import BuyerId


class BuyerRepository(Repository, ABC):
    @abstractmethod
    def add(self, Buyer):
        ...

    @abstractmethod
    def get(self, BuyerId):
        ...

    @abstractmethod
    def commit(self, Buyer):
        ...

    @abstractmethod
    def delete(self, Buyer):
        ...
