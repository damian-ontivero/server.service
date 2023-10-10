"""In memory message bus implementation."""

from st_server.shared.domain.value_object.domain_event import DomainEvent
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class InMemoryMessageBus(MessageBus):
    """In memory message bus implementation.

    The in memory message bus is a singleton.
    """

    _instance = None

    def __new__(cls) -> "InMemoryMessageBus":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = {}
        return cls._instance

    def subscribe(self, domain_event: DomainEvent, handler: callable) -> None:
        if domain_event not in self._handlers:
            self._handlers[domain_event] = []
        self._handlers[domain_event].append(handler)

    def publish(self, domain_events: list[DomainEvent]) -> None:
        for domain_event in domain_events:
            handlers = self._handlers.get(type(domain_event))
            if handlers:
                for handler in handlers:
                    handler(domain_event)
