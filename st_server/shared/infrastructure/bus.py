"""Abstract base class for buses."""

from abc import ABCMeta, abstractmethod

from st_server.shared.application.command import Command
from st_server.shared.application.query import Query
from st_server.shared.domain.domain_event import DomainEvent


class Bus(metaclass=ABCMeta):
    """Abstract base class for buses.

    A bus is a mechanism for dispatching commands, queries and publishing domain events.
    """

    @abstractmethod
    def dispatch(self, command: Command) -> None:
        """Dispatch a command."""
        raise NotImplementedError

    @abstractmethod
    def query(self, query: Query) -> object:
        """Query the application."""
        raise NotImplementedError

    @abstractmethod
    def publish(self, events: list[DomainEvent]) -> None:
        """Publish a list of domain events."""
        raise NotImplementedError
