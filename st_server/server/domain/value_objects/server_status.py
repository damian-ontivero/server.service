"""Value object that represents the status of the server."""


class ServerStatus:
    """Value object that represents the status of the server."""

    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"

    __slots__ = ("_value",)

    def __new__(cls, value: str) -> "ServerStatus":
        """Creates a new instance of server status."""
        if not isinstance(value, str):
            raise TypeError("Server status must be a string")
        if not len(value) > 0:
            raise ValueError("Server status cannot be empty")
        if value not in [cls.RUNNING, cls.STOPPED, cls.ERROR, cls.UNKNOWN]:
            raise ValueError("Invalid server status")
        self = object.__new__(cls)
        self.__setattr("_value", value)
        return self

    @classmethod
    def from_string(cls, value: str) -> "ServerStatus":
        """Named constructor for creating a server status from a string."""
        return cls(value=value)

    @property
    def value(self) -> str:
        """Returns the value of the server status."""
        return self._value

    @property
    def __dict__(self) -> dict:
        """Returns the dictionary representation of the server status."""
        return {"value": self.value}

    def __setattr__(self, name: str, value: object) -> None:
        """Prevents setting attributes."""
        raise AttributeError("Server status objects are immutable")

    def __delattr__(self, name: str) -> None:
        """Prevents deleting attributes."""
        raise AttributeError("Server status objects are immutable")

    def __eq__(self, other: object) -> bool:
        """Compares if two server status are equal."""
        if isinstance(other, ServerStatus):
            return self.value == other.value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two server status are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the server status."""
        return hash(self.value)

    def __repr__(self) -> str:
        """Returns the representation of the server status."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self.value
        )

    def __setattr(self, name: str, value: object) -> None:
        """Private method for setting attributes."""
        object.__setattr__(self, name, value)
