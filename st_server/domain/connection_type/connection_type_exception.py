"""Connection Type exception."""


class ConnectionTypeNotFound(Exception):
    """Custom error that is raised when a Connection Type with the provided id is not found."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Connection Type with the provided id is not found.

        Args:
            id (`int`): Connection Type id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"No Connection Type found with the provided id {self.id}."


class ConnectionTypeAlreadyExists(Exception):
    """Custom error that is raised when a Connection Type with the provided id already exists."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Connection Type with the provided id already exists.

        Args:
            id (`int`): Connection Type id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return (
            f"A Connection Type with the provided id {self.id} already exists."
        )


class ConnectionTypeNameAlreadyExists(Exception):
    """Custom error that is raised when a Connection Type with the provided name already exists."""

    def __init__(self, name: str) -> None:
        """Custom error that is raised when a Connection Type with the provided name already exists.

        Args:
            name (`str`): Connection Type name.
        """
        self.name = name

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Connection Type with the provided name {self.name} already exists."
