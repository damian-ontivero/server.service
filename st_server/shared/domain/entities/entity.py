"""Abstract base class for entities."""

from abc import ABCMeta, abstractmethod

from st_server.shared.domain.value_objects.domain_event import DomainEvent
from st_server.shared.domain.value_objects.entity_id import EntityId


class Entity(metaclass=ABCMeta):
    """Abstract base class for entities.

    Entities are domain objects with unique identity and defined by attributes.
    They have a specific life cycle: creation, update, and deletion. They are
    mutable and can be compared by their identity.
    """

    class Created(DomainEvent):
        """Domain event that represents the creation of the entity."""

        pass

    class Discarded(DomainEvent):
        """Domain event that represents the discarding of the entity."""

        pass

    @abstractmethod
    def __init__(self, id: EntityId, discarded: bool = False) -> None:
        """Initializes the entity."""
        self._id = id
        self._discarded = discarded

    @property
    def id(self) -> EntityId:
        """Returns the entity id."""
        return self._id

    @property
    def discarded(self) -> bool:
        """Returns whether the entity is discarded."""
        return self._discarded

    def __eq__(self, other: object) -> bool:
        """Compares if two entities are equal."""
        if isinstance(other, self.__class__):
            return self._id == other._id
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two entities are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the entity."""
        return hash(self._id)

    @abstractmethod
    def __repr__(self) -> str:
        """Returns the representation of the entity."""
        raise NotImplementedError

    def _check_not_discarded(self) -> None:
        """Checks if the entity is not discarded."""
        if self.discarded:
            raise ValueError("The entity is discarded")
