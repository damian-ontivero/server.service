"""Value object that represents the Entity id."""

from uuid import uuid4


class EntityId:
    """Value object that represents the Entity id."""

    __slots__ = ("_value",)

    def __new__(cls, value: str) -> "EntityId":
        """Creates a new instance of the Entity id."""
        if not isinstance(value, str):
            raise TypeError("EntityId must be a string")
        if not len(value) > 0:
            raise ValueError("EntityId must not be empty")
        self = object.__new__(cls)
        self.__setattr("_value", value)
        return self

    @classmethod
    def generate(cls) -> "EntityId":
        """Named constructor for generating a new Entity id."""
        return cls(value=uuid4().hex)

    @classmethod
    def from_text(cls, value: str) -> "EntityId":
        """Named constructor for creating an Entity id from a string."""
        return cls(value=value)

    @property
    def value(self) -> str:
        """Returns the value of the Entity id."""
        return self._value

    def __dict__(self) -> dict:
        """Returns the dictionary representation of the Entity id."""
        return {"value": self.value}

    def __setattr__(self, name: str, value: object) -> None:
        """Prevents setting attributes."""
        raise AttributeError("Entity id objects are immutable")

    def __delattr__(self, name: str) -> None:
        """Prevents deleting attributes."""
        raise AttributeError("Entity id objects are immutable")

    def __eq__(self, other: object) -> bool:
        """Compares if two Entity id are equal."""
        if isinstance(other, EntityId):
            return self.value == other.value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two Entity id are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the Entity id."""
        return hash(self.value)

    def __repr__(self) -> str:
        """Returns the representation of the Entity id."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self.value
        )

    def __setattr(self, name: str, value: object) -> None:
        """Private method for setting attributes."""
        object.__setattr__(self, name, value)
