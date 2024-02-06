class Environment:
    __slots__ = ("_value",)

    @classmethod
    def from_text(cls, text: str) -> "Environment":
        return cls(text)

    def __new__(cls, value: str) -> "Environment":
        if not isinstance(value, str):
            raise TypeError("Environment must be a string")
        if not len(value) > 0:
            raise ValueError("Environment cannot be empty")
        self = object.__new__(cls)
        self._value = value
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Environment):
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
