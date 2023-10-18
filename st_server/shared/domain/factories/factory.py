"""Abstract base class for factories."""

from abc import ABCMeta, abstractmethod

from st_server.shared.domain.entities.entity import Entity


class Factory(metaclass=ABCMeta):
    """Abstract base class for factories.

    Factories are used to build new entities or rebuild existing entities.
    """

    @staticmethod
    @abstractmethod
    def build(*args, **kwargs) -> Entity:
        """Abstract method to build a new Entity."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def rebuild(*args, **kwargs) -> Entity:
        """Abstract method to rebuild an existing Entity."""
        raise NotImplementedError
