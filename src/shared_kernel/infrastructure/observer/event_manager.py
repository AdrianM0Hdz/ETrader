from typing import DefaultDict, Set
from collections import defaultdict

from src.shared_kernel.application.observer.event_manager import EventManager
from src.shared_kernel.application.observer.subscriber import Subscriber
from src.shared_kernel.domain.events.event import Event


class ConcreteEventManager(EventManager):
    def __init__(self):
        self.events_to_subscribers: DefaultDict[type, Set[Subscriber]] = defaultdict(
            set
        )

    def subscribe(self, event_type: type, subscriber: Subscriber):
        self.events_to_subscribers[event_type].add(subscriber)

    def unsubscribe(self, event_type: type, subscriber: Subscriber):
        return self.events_to_subscribers[event_type].remove(subscriber)

    def notify(self, event_type: type, event: Event):
        for subscriber in self.events_to_subscribers[event_type]:
            subscriber.update(event)
