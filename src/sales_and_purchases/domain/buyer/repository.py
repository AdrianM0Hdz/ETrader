from abc import ABC, abstractmethod

from ..common.values import Name
from src.shared_kernel.domain.repository import Repository

from .buyer import Buyer
from .values import BuyerId


class BuyerRepository(Repository, ABC):
    @abstractmethod
    def add(self, item: Buyer):
        ...

    @abstractmethod
    def get(self, id: BuyerId):
        ...

    @abstractmethod
    def commit(self, item: Buyer):
        ...

    @abstractmethod
    def delete(self, item: Buyer):
        ...
