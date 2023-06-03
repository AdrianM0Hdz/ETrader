from abc import ABC, abstractmethod
from .aggregate_root import AggregateRoot
from .value_object import ValueObject


class Repository(ABC):
    @abstractmethod
    def add(self, item: AggregateRoot):
        ...

    @abstractmethod
    def get(self, id: ValueObject):
        ...

    @abstractmethod
    def commit(self, item: AggregateRoot):
        ...

    @abstractmethod
    def delete(self, item: AggregateRoot):
        ...
