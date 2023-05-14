"""Value object that represents the entity id."""

from uuid import uuid4


class EntityId:
    """Value object that represents the entity id."""

    def __init__(self, value: str = None) -> None:
        """Constructor.

        Args:
            value (`str`): Entity id. Defaults to None.
        """
        if value is None:
            self._value = uuid4().hex
        else:
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

    def __eq__(self, other) -> bool:
        """Compares two objects based on their value.

        Args:
            other (`object`): Object to compare.

        Returns:
            `bool`: True if both objects are equal.
        """
        if not isinstance(other, self.__class__):
            return False

        return self._value == other._value

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
        return "{c}(value='{v!r}')".format(
            c=self.__class__.__name__,
            v=self._value,
        )

    def __dict__(self) -> dict:
        """Returns the dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {"value": self._value}
