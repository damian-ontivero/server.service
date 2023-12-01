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
