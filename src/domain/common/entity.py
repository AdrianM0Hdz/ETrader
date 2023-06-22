from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from .value_object import ValueObject

TId = TypeVar("TId")


class Entity(ABC, Generic[TId]):
    @property
    def id(self) -> TId:
        return self._id

    @id.setter
    def id(self, new_id: TId) -> None:
        raise ValueError("ID OF AN ENTITY IS INMUTABLE")

    def __init__(self, id: TId):
        assert issubclass(type(id), ValueObject)
        self._id = id

    def __eq__(self, other_entity: "Entity") -> bool:
        return self.id == other_entity.id

    def __hash__(self) -> int:
        return hash(self._id)
