"""Value object that represents the Environment of the Server."""


class Environment:
    """Value object that represents the Environment of the Server."""

    __slots__ = ("_value",)

    def __new__(cls, value: str) -> "Environment":
        """Creates a new instance of Environment."""
        if not isinstance(value, str):
            raise TypeError("Environment must be a string")
        if not len(value) > 0:
            raise ValueError("Environment cannot be empty")
        self = object.__new__(cls)
        self.__setattr("_value", value)
        return self

    @classmethod
    def from_text(cls, value: str) -> "Environment":
        """Named constructor for creating an Environment from a string."""
        return cls(value=value)

    @property
    def value(self) -> str:
        """Returns the value of the Environment."""
        return self._value

    @property
    def __dict__(self) -> dict:
        """Returns the dictionary representation of the Environment."""
        return {"value": self.value}

    def __setattr__(self, name: str, value: object) -> None:
        """Prevents setting attributes."""
        raise AttributeError("Environment objects are immutable")

    def __delattr__(self, name: str) -> None:
        """Prevents deleting attributes."""
        raise AttributeError("Environment objects are immutable")

    def __eq__(self, other: object) -> bool:
        """Compares if two Environment are equal."""
        if isinstance(other, Environment):
            return self.value == other.value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two Environment are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the Environment."""
        return hash(self.value)

    def __repr__(self) -> str:
        """Returns the representation of the Environment."""
        return "{c}(value={value!r})".format(
            c=self.__class__.__name__, value=self.value
        )

    def __setattr(self, name: str, value: object) -> None:
        """Private method for setting attributes."""
        object.__setattr__(self, name, value)
