from typing import List
from uuid import uuid1

from ..common.aggregate_root import AggregateRoot
from ..common.values import Name

from ..seller.seller import Seller

from .values import BuyerId


class Buyer(AggregateRoot[BuyerId]):
    def __init__(self, id: BuyerId, name: Name):
        super().__init__(id)
        assert isinstance(name, Name)
        self.name = name
