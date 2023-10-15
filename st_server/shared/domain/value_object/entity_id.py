"""Value object that represents the Entity id."""

from uuid import uuid4


class EntityId:
    """Value object that represents the Entity id."""

    __slots__ = ("_value",)

    @classmethod
    def generate(cls) -> "EntityId":
        """Named constructor to create an Entity id."""
        return cls(uuid4().hex)

    @classmethod
    def from_text(cls, text: str) -> "EntityId":
        """Named constructor to create an Entity id from a string."""
        return cls(text)

    def __new__(cls, value: str) -> "EntityId":
        """Creates a new instance of the Entity id."""
        if not isinstance(value, str):
            raise TypeError("EntityId must be a string")
        if not len(value) > 0:
            raise ValueError("EntityId must not be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other: object) -> bool:
        """Compares if two Entity id are equal."""
        if isinstance(other, EntityId):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two Entity id are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the Entity id."""
        return hash(tuple(sorted(self._value)))

    def __repr__(self) -> str:
        """Returns the representation of the Entity id."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self) -> str:
        """Returns the value of the Entity id."""
        return self._value
