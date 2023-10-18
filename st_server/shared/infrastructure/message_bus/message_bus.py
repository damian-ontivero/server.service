"""Abstract base class for message bus."""

from abc import ABCMeta, abstractmethod

from st_server.shared.domain.value_objects.domain_event import DomainEvent


class MessageBus(metaclass=ABCMeta):
    """Abstract base class for message bus.

    A message bus is a mechanism for publishing and subscribing to messages.
    """

    @abstractmethod
    def publish(self, domain_events: list[DomainEvent]) -> None:
        """Publishes the domain events."""
        raise NotImplementedError
