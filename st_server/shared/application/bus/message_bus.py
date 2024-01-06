from abc import ABCMeta, abstractmethod

from st_server.shared.domain.domain_event import DomainEvent


class MessageBus(metaclass=ABCMeta):
    """Abstract base class for message bus.

    Message bus is a mechanism for publishing messages.
    """

    @abstractmethod
    def publish(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError
