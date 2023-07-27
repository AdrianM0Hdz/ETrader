from abc import ABC, abstractmethod
from src.shared_kernel.domain.events.event import Event

from .subscriber import Subscriber


class EventManager(ABC):
    @abstractmethod
    def subscribe(self, event_type: type, subcriber: Subscriber):
        ...

    @abstractmethod
    def unsubscribe(self, event_type: type, subscriber: Subscriber):
        ...

    @abstractmethod
    def notify(self, event_type: type, event: Event):
        ...
