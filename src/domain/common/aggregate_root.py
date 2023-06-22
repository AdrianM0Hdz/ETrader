from typing import TypeVar, Generic

from .value_object import ValueObject
from .entity import Entity


TId = TypeVar("TId")


class AggregateRoot(Entity[TId]):
    def __init__(self, id: TId):
        super().__init__(id)
