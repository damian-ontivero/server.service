"""Value object that represents the Environment of the Server."""


class Environment:
    """Value object that represents the Environment of the Server."""

    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, value):
        """Named constructor for creating an Environment from a string."""
        return cls(value)

    def __new__(cls, value):
        """Creates a new instance of Environment."""
        if not isinstance(value, str):
            raise TypeError("Environment must be a string")
        if not len(value) > 0:
            raise ValueError("Environment cannot be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other):
        """Compares if two Environment are equal."""
        if isinstance(other, Environment):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other):
        """Compares if two Environment are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Returns the hash of the Environment."""
        return hash(tuple(sorted(self._value)))

    def __repr__(self):
        """Returns the representation of the Environment."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self):
        """Returns the value of the Environment."""
        return self._value
