from abc import ABCMeta, abstractmethod

from st_server.shared.domain.entity_id import EntityId


class Entity(metaclass=ABCMeta):
    """Abstract base class for entities.

    Entities are domain objects with unique identity and defined by attributes.
    They have a specific life cycle: creation, update, and deletion. They are
    mutable and can be compared by their identity.
    """

    @abstractmethod
    def __init__(self, id: EntityId, discarded: bool = False) -> None:
        """Initializes the entity."""
        if id is None:
            raise ValueError("Entity ID must not be None")
        self._id = id
        self._discarded = discarded

    def __eq__(self, other: object) -> bool:
        """Checks if two entities are equal."""
        if isinstance(other, self.__class__):
            return self._id == other._id
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Checks if two entities are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the entity."""
        return hash(self._id)

    @property
    def id(self) -> EntityId:
        """Returns the entity ID."""
        self._check_not_discarded()
        return self._id

    @property
    def discarded(self) -> bool:
        """Returns whether the entity is discarded."""
        return self._discarded

    def _check_not_discarded(self) -> None:
        """Checks if the entity is not discarded."""
        if self.discarded:
            raise DiscardedEntityError("The entity is discarded")


class DiscardedEntityError(Exception):
    """Exception raised when an operation is attempted on a discarded entity."""

    pass
