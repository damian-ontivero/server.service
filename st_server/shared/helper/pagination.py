"""Validates pagination attributes."""

from functools import wraps

from st_server.shared.core.exception import PaginationError


def validate_pagination(func):
    """Validates pagination attributes."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Doc."""
        limit = kwargs.get("limit", None)
        offset = kwargs.get("offset", None)

        if limit is not None:
            try:
                assert int(limit) >= 0

            except ValueError:
                raise PaginationError(
                    "The limit number must be an integer value"
                )

            except AssertionError:
                raise PaginationError("The limit number cannot be less than 1")

        if offset is not None:
            try:
                assert int(offset) >= 0

            except ValueError:
                raise PaginationError(
                    "The offset number must be an integer value"
                )

            except AssertionError:
                raise PaginationError(
                    "The offset number cannot be less than 0"
                )

        return func(*args, **kwargs)

    return wrapped
