"""Abstract base class for query handlers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.application.query import Query


class QueryHandler(metaclass=ABCMeta):
    """Abstract base class for query handlers."""

    @abstractmethod
    def handle(self, query: Query) -> None:
        """Handle the query."""
        raise NotImplementedError
