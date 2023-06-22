""" 
Value object implementation
"""

from typing import Tuple
from abc import ABC, abstractmethod


class ValueObject(ABC):
    @abstractmethod
    def get_equality_componets(self) -> Tuple:
        ...

    def __eq__(self, other: "ValueObject") -> bool:
        if type(self) != type(other):
            raise ValueError(f"Object of different type from {type(self)}")
        if self.get_equality_componets() != other.get_equality_componets():
            return False
        return True

    def __hash__(self) -> int:
        hash_code = 0
        for value in self.get_equality_componets():
            hash_code ^= hash(value)
        return hash_code
