"""Operating System exception."""


class OperatingSystemNotFound(Exception):
    """Custom error that is raised when a Operating System with the provided id is not found."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Operating System with the provided id is not found.

        Args:
            id (`int`): Operating System id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"No Operating System found with id {self.id}."


class OperatingSystemAlreadyExists(Exception):
    """Custom error that is raised when a Operating System with the provided id already exists."""

    def __init__(self, id: int) -> None:
        """Custom error that is raised when a Operating System with the provided id already exists.

        Args:
            id (`int`): Operating System id.
        """
        self.id = id

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Operating System with id {self.id} already exists."


class OperatingSystemNameAlreadyExists(Exception):
    """Custom error that is raised when a Operating System with the provided name already exists."""

    def __init__(self, name: str) -> None:
        """Custom error that is raised when a Operating System with the provided name already exists.

        Args:
            name (`str`): Operating System name.
        """
        self.name = name

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return f"A Operating System with name {self.name} already exists."
