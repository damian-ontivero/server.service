"""Value object that represents an operating system."""


class OperatingSystem:
    """Value object that represents an operating system."""

    def __init__(self, name: str, version: str, architect: str) -> None:
        """Constructor.

        Args:
            name (`str`): Operating system name.
            version (`str`): Operating system version.
            architect (`str`): Operating system architect.
        """
        self._name = name
        self._version = version
        self._architect = architect

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

    @property
    def version(self) -> str:
        """Returns the connection type name.

        Returns:
            `str`: Connection type name.
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """Raises an exception.

        Raises:
            `AttributeError`: The version attribute is read-only.
        """
        raise AttributeError("The version attribute is read-only.")

    @property
    def architect(self) -> str:
        """Returns the connection type name.

        Returns:
            `str`: Connection type name.
        """
        return self._architect

    @architect.setter
    def architect(self, value: str) -> None:
        """Raises an exception.

        Raises:
            `AttributeError`: The architect attribute is read-only.
        """
        raise AttributeError("The architect attribute is read-only.")

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
        return (
            f"{self.__class__.__name__}(name={self._name}, "
            f"version={self._version}, architect={self._architect})"
        )

    def __dict__(self) -> dict:
        """Returns the dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {
            "name": self._name,
            "version": self._version,
            "architect": self._architect,
        }
