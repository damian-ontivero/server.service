"""Value object that represents the Connection Type of the Credential."""


class ConnectionType:
    """Value object that represents the Connection Type of the Credential."""

    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, value):
        """Named constructor for creating a Connection Type from a string."""
        return cls(value)

    def __new__(cls, value):
        """Creates a new instance of Connection Type."""
        if not isinstance(value, str):
            raise TypeError("Connection type must be a string")
        if not len(value) > 0:
            raise ValueError("Connection type cannot be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other):
        """Compares if two Connection Type are equal."""
        if isinstance(other, ConnectionType):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other):
        """Compares if two Connection Type are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Returns the hash of the Connection Type."""
        return hash(tuple(sorted(self._value)))

    def __repr__(self):
        """Returns the representation of the Connection Type."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self):
        """Returns the value of the Connection Type."""
        return self._value
