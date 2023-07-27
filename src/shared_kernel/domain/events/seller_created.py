from dataclasses import dataclass
from uuid import uuid1

from .event import Event


@dataclass(frozen=True)
class SellerCreated(Event):
    seller_id: str

    @classmethod
    def create_new(cls, seller_id: str) -> "SellerCreated":
        return cls(id=str(uuid1()), seller_id=seller_id)
