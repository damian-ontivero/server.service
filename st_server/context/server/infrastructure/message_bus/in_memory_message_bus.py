"""In memory message bus implementation."""

from st_server.shared.domain_event import DomainEvent
from st_server.shared.message_bus import MessageBus


class InMemoryMessageBus(MessageBus):
    """In memory message bus implementation."""

    _instance = None

    def __new__(cls) -> "InMemoryMessageBus":
        """Singleton instance of the in memory message bus.

        Returns:
            `InMemoryMessageBus`: Singleton instance of the in memory message bus.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = {}

        return cls._instance

    def subscribe(self, domain_event: DomainEvent, handler: callable) -> None:
        """Subscribes to domain events.

        Args:
            domain_event (`DomainEvent`): Domain event to subscribe to.
            handler (`callable`): Handler to execute when the domain event is published.
        """
        if domain_event not in self._handlers:
            self._handlers[domain_event] = []

        self._handlers[domain_event].append(handler)

    def publish(self, domain_events: list[DomainEvent]) -> None:
        """Publishes domain events.

        Args:
            domain_events (`list[DomainEvent]`): Domain events to publish.
        """
        for domain_event in domain_events:
            handlers = self._handlers.get(type(domain_event))

            if handlers:
                for handler in handlers:
                    handler(domain_event)
