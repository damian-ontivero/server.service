"""Domain exceptions."""


class NotFound(Exception):
    """Exception raised when an entity is not found."""

    pass


class AlreadyExists(Exception):
    """Exception raised when an entity already exists."""

    pass


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""

    pass


class PasswordError(Exception):
    """Exception raised when a password is incorrect."""

    pass


class PaginationError(Exception):
    """Exception raised when pagination fails."""

    pass


class FilterError(Exception):
    """Exception raised when a filter is incorrect."""

    pass


class SortError(Exception):
    """Exception raised when a sort is incorrect."""

    pass
