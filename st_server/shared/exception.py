"""Domain exceptions."""


class NotFound(Exception):
    """Custom error that is raised when an entity is not found."""

    def __init__(self, message: str | None = None) -> None:
        """Custom error that is raised when an entity is not found.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message or "Entity not found."


class AlreadyExists(Exception):
    """Custom error that is raised when an entity already exists."""

    def __init__(self, message: str | None = None) -> None:
        """Custom error that is raised when an entity already exists.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message or "Entity already exists."


class AuthenticationError(Exception):
    """Custom error that is raised when the authentication fails."""

    def __init__(self, message: str | None = None) -> None:
        """Custom error that is raised when the authentication fails.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message or "Authentication failed."


class PaginationError(Exception):
    """Custom error that is raised when pagination fails."""

    def __init__(self, message: str | None = None) -> None:
        """Custom error that is raised when pagination fails.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message or "Pagination failed."


class FilterError(Exception):
    """Custom error that is raised when the filter fails."""

    def __init__(self, message: str | None = None) -> None:
        """Custom error that is raised when the filter fails.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message or "Incorrect filter format."


class SortError(Exception):
    """Custom error that is raised when the sort fails."""

    def __init__(self, message: str | None = None) -> None:
        """Custom error that is raised when the sort fails.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        self.message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return (
            self.message
            or "Incorrect sort format. Valid format: 'name:asc' or 'name:desc'."
        )
