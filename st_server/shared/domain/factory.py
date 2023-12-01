"""Abstract base class for factories."""

from abc import ABCMeta, abstractmethod

from st_server.shared.domain.aggregate_root import AggregateRoot


class Factory(metaclass=ABCMeta):
    """Abstract base class for factories.

    Factories are used to build and rebuild aggregate roots.
    """

    @staticmethod
    @abstractmethod
    def build(*args, **kwargs) -> AggregateRoot:
        """Builds a new aggregate root."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def rebuild(*args, **kwargs) -> AggregateRoot:
        """Rebuilds an existing aggregate root."""
        raise NotImplementedError
