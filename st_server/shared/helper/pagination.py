"""Validates pagination attributes."""

from functools import wraps

from st_server.shared.application.exception.exception import PaginationError


def validate_pagination(func):
    """Decorator to validate pagination attributes."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        _limit = kwargs.get("_limit", None)
        _offset = kwargs.get("_offset", None)

        if _limit is not None:
            try:
                assert int(_limit) >= 0
            except ValueError:
                raise PaginationError(
                    "The _limit number must be an integer value"
                )
            except AssertionError:
                raise PaginationError(
                    "The _limit number cannot be less than 1"
                )
        if _offset is not None:
            try:
                assert int(_offset) >= 0
            except ValueError:
                raise PaginationError(
                    "The _offset number must be an integer value"
                )
            except AssertionError:
                raise PaginationError(
                    "The _offset number cannot be less than 0"
                )
        return func(*args, **kwargs)

    return wrapped
