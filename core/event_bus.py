from collections import defaultdict
from typing import Callable


class EventBus:
    """Bus de eventos para desacoplar componentes del sistema."""

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable):
        self._subscribers[event].append(handler)

    def publish(self, event: str, payload: dict):
        for handler in self._subscribers[event]:
            handler(payload)


bus = EventBus()
