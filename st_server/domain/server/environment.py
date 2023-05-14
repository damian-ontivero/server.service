"""Value object that represents an environment."""


class Environment:
    """Value object that represents an environment."""

    def __init__(self, name: str = None) -> None:
        """Constructor.

        Args:
            name (`str`): Environment name.
        """
        self._name = name

    @property
    def name(self) -> str:
        """Returns the connection type name.

        Returns:
            `str`: Connection type name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Raises an exception.

        Raises:
            `AttributeError`: The name attribute is read-only.
        """
        raise AttributeError("The name attribute is read-only.")

    def __eq__(self, other) -> bool:
        """Compares two objects based on their values.

        Args:
            other (`object`): Object to compare.

        Returns:
            `bool`: True if both objects are equal.
        """
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Returns the hash value of the object.

        Returns:
            `int`: Hash value of the object.
        """
        return hash((self.__class__.__name__, self.__dict__))

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return f"{self.__class__.__name__}(name={self._name})"

    def __dict__(self) -> dict:
        """Returns the dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {"name": self._name}
