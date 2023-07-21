from typing import List
from dataclasses import dataclass
from uuid import uuid1

from src.shared_kernel.domain.aggregate_root import AggregateRoot
from ..common.values import Name
from .values import BuyerId


# everything needs to be a value due to inmutability


class Buyer(AggregateRoot[BuyerId]):
    def __init__(self, id: BuyerId, name: Name):
        super().__init__(id)
        assert isinstance(name, Name)
        self.name = name

    @classmethod
    def create_new(cls, name: Name):
        return cls(BuyerId(str(uuid1())), name)
