from abc import ABCMeta, abstractmethod

from st_server.shared.application.query import Query


class QueryHandler(metaclass=ABCMeta):
    """Abstract base class for query handlers.

    This class represents the blueprint for handling queries within the application.
    """

    @abstractmethod
    def handle(self, query: Query) -> None:
        raise NotImplementedError
