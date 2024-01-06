class ServerStatus:
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"

    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, text: str) -> "ServerStatus":
        return cls(text)

    def __new__(cls, value: str) -> "ServerStatus":
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
        if isinstance(other, ServerStatus):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self._value
        )

    @property
    def value(self) -> str:
        return self._value
