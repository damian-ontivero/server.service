"""Abstract base class for entities."""

from abc import ABCMeta, abstractmethod

from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class Entity(metaclass=ABCMeta):
    """Abstract base class for entities.

    Entities are domain objects with unique identity and defined by attributes.
    They have a specific life cycle: creation, update, and deletion. They are
    mutable and can be compared by their identity.
    """

    class Created(DomainEvent):
        """Domain event for entity created."""

        pass

    class Discarded(DomainEvent):
        """Domain event for entity discarded."""

        pass

    @abstractmethod
    def __init__(self, id: EntityId, discarded: bool = False) -> None:
        """Initializes the entity.

        Args:
            id (`EntityId`): Entity id.
            discarded (`bool`): Indicates if the entity is discarded.
        """
        self._id = id
        self._discarded = discarded

    @property
    def id(self) -> str:
        """Returns the entity id.

        Returns:
            `str`: Entity id.
        """
        return self._id

    @property
    def discarded(self) -> bool:
        """Returns True if the entity is discarded.

        Returns:
            `bool`: True if the entity is discarded.
        """
        return self._discarded

    def __eq__(self, other) -> bool:
        """Compares two objects based on their id.

        Args:
            other (`object`): Object to compare.

        Returns:
            `bool`: True if both objects are equal.
        """
        if not isinstance(other, self.__class__):
            return False

        return self._id == other._id

    def __hash__(self) -> int:
        """Returns the hash value of the object.

        Returns:
            `int`: Hash value of the object.
        """
        return hash((self.__class__.__name__, self._id))

    @abstractmethod
    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        raise NotImplementedError

    def check_not_discarded(self) -> None:
        """Raises an exception if the entity is discarded.

        Raises:
            `ValueError`: If the entity is discarded.
        """
        if self._discarded:
            raise ValueError("The entity is discarded.")

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_dict(data: dict) -> "Entity":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `Entity`: Instance of the class.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create() -> None:
        """Entity factory method.

        Important:
            This method is only used to create a new entity.
            When creating a new entity, the id is automatically generated
            and a domain event is registered.
        """
        raise NotImplementedError

    @abstractmethod
    def discard(self) -> None:
        """Entity discard method.

        Important:
            This method is only used to discard an entity.
            When discarding an entity, the discarded attribute is set to True
            and a domain event is registered.
        """
        raise NotImplementedError
