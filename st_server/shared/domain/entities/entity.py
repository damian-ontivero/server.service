"""Abstract base class for entities."""

from abc import ABCMeta, abstractmethod

from st_server.shared.domain.value_objects.entity_id import EntityId


class Entity(metaclass=ABCMeta):
    """Abstract base class for entities.

    Entities are domain objects with unique identity and defined by attributes.
    They have a specific life cycle: creation, update, and deletion. They are
    mutable and can be compared by their identity.
    """

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
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two entities are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the entity."""
        return hash((self.__class__.__name__, self._id.value))

    @abstractmethod
    def __repr__(self) -> str:
        """Returns the representation of the entity."""
        raise NotImplementedError

    def _check_not_discarded(self) -> None:
        """Checks if the entity is not discarded."""
        if self.discarded:
            raise ValueError("The entity is discarded")

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the entity."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(data: dict) -> "Entity":
        """Named constructor for creating an entity from a dictionary."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create() -> "Entity":
        """Named constructor for creating a new entity."""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> "Entity":
        """Updates the entity."""
        raise NotImplementedError

    @abstractmethod
    def discard(self) -> None:
        """Discards the entity."""
        raise NotImplementedError
