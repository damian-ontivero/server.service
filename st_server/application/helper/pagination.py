"""Exceptions and decorator to validate pagination attributes."""

from functools import wraps

from st_server.domain.exception import PaginationError


def validate_pagination(func):
    """Decorator to validate pagination attributes."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Doc."""
        per_page = kwargs.get("per_page", None)
        page = kwargs.get("page", None)

        if per_page is not None:
            try:
                assert int(per_page) >= 0
            except ValueError:
                raise PaginationError(
                    message="The number of records per page must be an integer value."
                )
            except AssertionError:
                raise PaginationError(
                    message="The number of records per page cannot be less than 0."
                )

        if page is not None:
            try:
                assert int(page) >= 1
            except ValueError:
                raise PaginationError(
                    message="The page number must be an integer value."
                )
            except AssertionError:
                raise PaginationError(
                    message="The page number cannot be less than 1."
                )

        return func(*args, **kwargs)

    return wrapped
