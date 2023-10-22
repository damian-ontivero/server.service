"""Value object that represents the Connection Type of the Credential."""


class ConnectionType:
    """Value object that represents the Connection Type of the Credential."""

    __slots__ = ("_value",)

    def __new__(cls, value: str) -> "ConnectionType":
        """Creates a new instance of Connection Type."""
        if not isinstance(value, str):
            raise TypeError("Connection type must be a string")
        if not len(value) > 0:
            raise ValueError("Connection type cannot be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    @property
    def value(self) -> str:
        """Returns the value of the Connection Type."""
        return self._value

    @classmethod
    def from_text(cls, text: str) -> "ConnectionType":
        """Named constructor to create a Connection Type from a string."""
        return cls(text)

    def __eq__(self, other: object) -> bool:
        """Compares if two Connection Type are equal."""
        if isinstance(other, ConnectionType):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two Connection Type are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the Connection Type."""
        return hash(self._value)

    def __repr__(self) -> str:
        """Returns the representation of the Connection Type."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )