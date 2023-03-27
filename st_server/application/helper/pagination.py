"""Exceptions and decorator to validate pagination attributes."""

from functools import wraps


class PageNotAnInteger(Exception):
    """Custom error that is raised when the page number is not an integer."""

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return "The page number must be an integer value."


class PageLessThanOne(Exception):
    """Custom error that is raised when the page number is less than 1."""

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return "The page number cannot be less than 1."


class PerPageNotAnInteger(Exception):
    """Custom error that is raised when the number of records per page is not an integer."""

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return "The number of records per page must be an integer value."


class PerPageLessThanZero(Exception):
    """Custom error that is raised when the number of records is less than 0."""

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return "The number of records per page cannot be less than 0."


def validate_pagination(func):
    """Decorator to validate pagination attributes."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Doc."""
        per_page = kwargs.get("per_page", None)
        page = kwargs.get("page", None)

        if per_page is not None:
            try:
                per_page = int(per_page)

                assert per_page >= 0

            except ValueError:
                raise PerPageNotAnInteger

            except AssertionError:
                raise PerPageLessThanZero

        if page is not None:
            try:
                page = int(page)

                assert page >= 1

            except ValueError:
                raise PageNotAnInteger

            except AssertionError:
                raise PageLessThanOne

        return func(*args, **kwargs)

    return wrapped
