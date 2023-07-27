from dataclasses import dataclass
from uuid import uuid1

from .event import Event


@dataclass(frozen=True)
class BuyerCreated(Event):
    buyer_id: str

    @classmethod
    def create_new(cls, buyer_id: str) -> "BuyerCreated":
        return cls(id=str(uuid1()), buyer_id=buyer_id)
