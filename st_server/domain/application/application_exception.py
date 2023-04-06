"""Application exception."""


class ApplicationNotFound(Exception):
    """Custom error that is raised when a Application with the provided id is not found."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Application with the provided id is not found.

        Args:
            id (`int`): Application id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"No Application found with the provided id {self.id}."


class ApplicationAlreadyExists(Exception):
    """Custom error that is raised when a Application with the provided id already exists."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Application with the provided id already exists.

        Args:
            id (`int`): Application id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Application with the provided id {self.id} already exists."


class ApplicationNameAlreadyExists(Exception):
    """Custom error that is raised when a Application with the provided name already exists."""

    def __init__(self, name: str) -> None:
        """Custom error that is raised when a Application with the provided name already exists.

        Args:
            name (`str`): Application name.
        """
        self.name = name

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return (
            f"A Application with the provided name {self.name} already exists."
        )
