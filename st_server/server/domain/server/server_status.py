class ServerStatus:
    """Value object that represents the status of the Server."""

    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"

    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, text: str) -> "ServerStatus":
        """Named constructor to create the value object from a text."""
        return cls(text)

    def __new__(cls, value: str) -> "ServerStatus":
        """Creates a new instance of the value object."""
        if not isinstance(value, str):
            raise TypeError("Server status must be a string")
        if not len(value) > 0:
            raise ValueError("Server status cannot be empty")
        if value not in [cls.RUNNING, cls.STOPPED, cls.ERROR, cls.UNKNOWN]:
            raise ValueError("Invalid Server status")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other: object) -> bool:
        """Checks if two value objects are equal."""
        if isinstance(other, ServerStatus):
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
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self) -> str:
        """Returns the value."""
        return self._value
