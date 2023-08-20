"""Domain exceptions."""


class NotFound(Exception):
    """Exception raised when an entity is not found."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Entity not found"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message


class AlreadyExists(Exception):
    """Exception raised when an entity already exists."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Entity already exists"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Authentication failed"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message


class PasswordError(Exception):
    """Exception raised when a password is incorrect."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Password is incorrect"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message


class PaginationError(Exception):
    """Exception raised when pagination fails."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Pagination failed"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message


class FilterError(Exception):
    """Exception raised when a filter is incorrect."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Incorrect filter format"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message


class SortError(Exception):
    """Exception raised when a sort is incorrect."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the exception."""
        if message is None:
            message = "Incorrect sort format'"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        """Returns the string representation of the exception."""
        return self._message
