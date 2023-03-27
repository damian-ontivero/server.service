"""Server exception."""


class ServerNotFound(Exception):
    """Custom error that is raised when a Server with the provided id is not found."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Server with the provided id is not found.

        Args:
            id (`int`): Server id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"No Server found with id {self.id}."


class ServerAlreadyExists(Exception):
    """Custom error that is raised when a Server with the provided id already exists."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Server with the provided id already exists.

        Args:
            id (`int`): Server id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Server with id {self.id} already exists."


class ServerNameAlreadyExists(Exception):
    """Custom error that is raised when a Server with the provided name already exists."""

    def __init__(self, name: str) -> None:
        """Custom error that is raised when a Server with the provided name already exists.

        Args:
            name (`str`): Server name.
        """
        self.name = name

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Server with name {self.name} already exists."
