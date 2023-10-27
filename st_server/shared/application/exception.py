"""Exceptions raised by the application."""


class NotFound(Exception):
    pass


class AlreadyExists(Exception):
    pass


class AuthenticationError(Exception):
    pass


class PasswordError(Exception):
    pass


class PaginationError(Exception):
    pass


class FilterError(Exception):
    pass


class SortError(Exception):
    pass


class HandlerNotRegistered(Exception):
    pass
