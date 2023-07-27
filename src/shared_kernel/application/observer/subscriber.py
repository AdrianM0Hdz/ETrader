from abc import ABC, abstractmethod
from src.shared_kernel.domain.events.event import Event


class Subscriber(ABC):
    @abstractmethod
    def update(self, event: Event):
        ...
