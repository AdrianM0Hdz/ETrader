from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    id: str
