"""Value object that represents the status of the Server."""


class ServerStatus:
    """Value object that represents the status of the Server."""

    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"

    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, value):
        """Named constructor for creating a Server status from a string."""
        return cls(value)

    def __new__(cls, value):
        """Creates a new instance of Server status."""
        if not isinstance(value, str):
            raise TypeError("Server status must be a string")
        if not len(value) > 0:
            raise ValueError("Server status cannot be empty")
        if value not in [cls.RUNNING, cls.STOPPED, cls.ERROR, cls.UNKNOWN]:
            raise ValueError("Invalid Server status")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other):
        """Compares if two Server status are equal."""
        if isinstance(other, ServerStatus):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other):
        """Compares if two Server status are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Returns the hash of the Server status."""
        return hash(tuple(sorted(self._value)))

    def __repr__(self):
        """Returns the representation of the Server status."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self):
        """Returns the value of the Server status."""
        return self._value
