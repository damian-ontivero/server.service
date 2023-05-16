"""Abc for message bus."""

from abc import ABCMeta, abstractmethod

from st_server.shared.core.domain_event import DomainEvent


class MessageBus(metaclass=ABCMeta):
    """Abc for message bus."""

    @abstractmethod
    def publish(self, domain_events: list[DomainEvent]) -> None:
        """Publishes domain events.

        Args:
            domain_events (`list[DomainEvent]`): Domain events to publish.
        """
        raise NotImplementedError
