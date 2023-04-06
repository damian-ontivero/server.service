"""Environment exception."""


class EnvironmentNotFound(Exception):
    """Custom error that is raised when a Environment with the provided id is not found."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Environment with the provided id is not found.

        Args:
            id (`int`): Environment id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"No Environment found with the provided id {self.id}."


class EnvironmentAlreadyExists(Exception):
    """Custom error that is raised when a Environment with the provided id already exists."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Environment with the provided id already exists.

        Args:
            id (`int`): Environment id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Environment with the provided id {self.id} already exists."


class EnvironmentNameAlreadyExists(Exception):
    """Custom error that is raised when a Environment with the provided name already exists."""

    def __init__(self, name: str) -> None:
        """Custom error that is raised when a Environment with the provided name already exists.

        Args:
            name (`str`): Environment name.
        """
        self.name = name

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return (
            f"A Environment with the provided name {self.name} already exists."
        )
