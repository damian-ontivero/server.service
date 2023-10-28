"""Exceptions raised by the application."""


class NotFound(Exception):
    """Raised when a resource is not found."""

    pass


class AlreadyExists(Exception):
    """Raised when a resource already exists."""

    pass


class AuthenticationError(Exception):
    """Raised when a user fails to authenticate."""

    pass


class PasswordError(Exception):
    """Raised when a password is invalid."""

    pass


class PaginationError(Exception):
    """Raised when pagination fails."""

    pass


class FilterError(Exception):
    """Raised when filtering fails."""

    pass


class SortError(Exception):
    """Raised when sorting fails."""

    pass


class HandlerNotRegistered(Exception):
    """Raised when a handler is not registered."""

    pass
