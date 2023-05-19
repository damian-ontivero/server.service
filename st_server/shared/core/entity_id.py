"""Value object that represents the entity id."""

from typing import Any
from uuid import uuid4


class EntityId:
    """Value object that represents the entity id."""

    def __init__(self, value: str = None) -> None:
        """Constructor.

        Args:
            value (`str`): Entity id. Defaults to None.
        """
        if value is None:
            value = uuid4().hex

        self._value = value

    @property
    def value(self) -> str:
        """Returns the entity id.

        Returns:
            `str`: Entity id.
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Raises an exception.

        Raises:
            `AttributeError`: The value attribute is read-only.
        """
        raise AttributeError("The value attribute is read-only.")

    def __eq__(self, rhs: Any) -> bool:
        """Compares two objects based on their access token.

        Args:
            rhs (`Any`): Right hand side object to compare.

        Returns:
            `bool`: True if both objects are equal.
        """
        if not isinstance(rhs, self.__class__):
            return NotImplemented

        return self._value == rhs._value

    def __hash__(self) -> int:
        """Returns the hash value of the object.

        Returns:
            `int`: Hash value of the object.
        """
        return hash((self.__class__.__name__, self._value))

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return f"{self.__class__.__name__}(value={self._value})"

    def __dict__(self) -> dict:
        """Returns the dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {"value": self._value}
