class ConnectionType:
    """Value object that represents the Connection Type of the Credential."""

    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, text: str) -> "ConnectionType":
        """Named constructor to create the value object from a text."""
        return cls(text)

    def __new__(cls, value: str) -> "ConnectionType":
        """Creates a new instance of the value object."""
        if not isinstance(value, str):
            raise TypeError("Connection type must be a string")
        if not len(value) > 0:
            raise ValueError("Connection type cannot be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other: object) -> bool:
        """Checks if two value objects are equal."""
        if isinstance(other, ConnectionType):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Checks if two value objects are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the value object."""
        return hash(self._value)

    def __repr__(self) -> str:
        """Returns the string representation of the value object."""
        return f"{self.__class__.__name__}(value={self._value!r})"

    @property
    def value(self) -> str:
        """Returns the value."""
        return self._value
