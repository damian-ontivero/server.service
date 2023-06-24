"""Abstract base class for entities."""

from abc import ABCMeta, abstractmethod
from typing import Any

from st_server.shared.core.entity_id import EntityId


class Entity(metaclass=ABCMeta):
    """Abstract base class for entities.

    Entities are domain objects with unique identity and defined by attributes.
    They have a specific life cycle: creation, update, and deletion. They are
    mutable and can be compared by their identity.
    """

    @abstractmethod
    def __init__(self, id: EntityId, discarded: bool = False) -> None:
        self._id = id
        self._discarded = discarded

    @property
    def id(self) -> EntityId:
        return self._id

    @property
    def discarded(self) -> bool:
        return self._discarded

    def __eq__(self, rhs: Any) -> bool:
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._id == rhs.id

    def __ne__(self, rhs: Any) -> bool:
        return not self.__eq__(rhs)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._id))

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    def _check_not_discarded(self) -> None:
        if self._discarded:
            raise ValueError("The entity is discarded")

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(data: dict) -> "Entity":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create() -> "Entity":
        raise NotImplementedError

    @abstractmethod
    def update(self) -> "Entity":
        raise NotImplementedError

    @abstractmethod
    def discard(self) -> None:
        raise NotImplementedError
