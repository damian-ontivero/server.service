"""Domain exceptions."""


class NotFound(Exception):
    """Exception raised when an entity is not found."""


class AlreadyExists(Exception):
    """Exception raised when an entity already exists."""


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""


class PasswordError(Exception):
    """Exception raised when a password is incorrect."""


class PaginationError(Exception):
    """Exception raised when pagination fails."""


class FilterError(Exception):
    """Exception raised when a filter is incorrect."""


class SortError(Exception):
    """Exception raised when a sort is incorrect."""
