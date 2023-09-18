"""Value object that represents the Entity id."""

from uuid import uuid4


class EntityId:
    """Value object that represents the Entity id."""

    __slots__ = ("_value",)

    @classmethod
    def generate(cls):
        """Named constructor for generating a new Entity id."""
        return cls(uuid4().hex)

    @classmethod
    def from_text(cls, value):
        """Named constructor for creating an Entity id from a string."""
        return cls(value)

    def __new__(cls, value):
        """Creates a new instance of the Entity id."""
        if not isinstance(value, str):
            raise TypeError("EntityId must be a string")
        if not len(value) > 0:
            raise ValueError("EntityId must not be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other):
        """Compares if two Entity id are equal."""
        if isinstance(other, EntityId):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other):
        """Compares if two Entity id are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Returns the hash of the Entity id."""
        return hash(tuple(sorted(self._value)))

    def __repr__(self):
        """Returns the representation of the Entity id."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self):
        """Returns the value of the Entity id."""
        return self._value
