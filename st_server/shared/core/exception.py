"""Domain exceptions."""


class NotFound(Exception):
    """Custom error that is raised when an entity is not found."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes a new instance of the NotFound class.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        if message is None:
            message = "Entity not found"

        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message


class AlreadyExists(Exception):
    """Custom error that is raised when an entity already exists."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes a new instance of the AlreadyExists class.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        if message is None:
            message = "Entity already exists"

        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message


class AuthenticationError(Exception):
    """Custom error that is raised when the authentication fails."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes a new instance of the AuthenticationError class.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        if message is None:
            message = "Authentication failed"

        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message


class PaginationError(Exception):
    """Custom error that is raised when pagination fails."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes a new instance of the PaginationError class.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        if message is None:
            message = "Pagination failed"

        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message


class FilterError(Exception):
    """Custom error that is raised when the filter fails."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes a new instance of the FilterError class.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        if message is None:
            message = "Incorrect filter format"

        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self._message


class SortError(Exception):
    """Custom error that is raised when the sort fails."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes a new instance of the SortError class.

        Args:
            message (`str` | `None`): Error message. Defaults to `None`.
        """
        if message is None:
            message = "Incorrect sort format. Valid format: 'name:asc' or 'name:desc'"

        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return self.message
