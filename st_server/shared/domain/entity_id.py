from uuid import uuid4


class EntityId:
    """Value object that represents an entity identifier."""

    __slots__ = ("_value",)

    @classmethod
    def generate(cls) -> "EntityId":
        """Named constructor to generate a new value object."""
        return cls(uuid4().hex)

    @classmethod
    def from_text(cls, text: str) -> "EntityId":
        """Named constructor to create the value object from a text."""
        return cls(text)

    def __new__(cls, value: str) -> "EntityId":
        """Creates a new instance of the value object."""
        if not isinstance(value, str):
            raise TypeError("Entity identifier must be a string")
        if not value:
            raise ValueError("Entity identifier must not be empty")
        self = super().__new__(cls)
        self._value = value
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EntityId):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value!r})"

    @property
    def value(self) -> str:
        return self._value
