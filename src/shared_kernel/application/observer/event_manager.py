from abc import ABC, abstractmethod
from src.shared_kernel.domain.events.event import Event

from .subscriber import Subscriber


class EventManager(ABC):
    @abstractmethod
    def subscribe(self, event: Event, subcriber: Subscriber):
        ...

    @abstractmethod
    def unsubscribe(self, event: Event, subscriber: Subscriber):
        ...

    @abstractmethod
    def notify(self, event_type: type, event: Event):
        ...
