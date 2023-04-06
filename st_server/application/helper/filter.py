"""Exceptions and decorator to validate filter format."""

from functools import wraps

KNOWN_PARAMS = [
    "per_page",
    "page",
    "sort",
    "access_token",
]
OPERATORS = [
    "eq",
    "gt",
    "ge",
    "lt",
    "le",
    "in",
    "btw",
    "lk",
]


class FilterFormatError(Exception):
    """Custom error that is raised when the filter format is incorrect."""

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return "Incorrect filter format."


def validate_filter(func):
    """Decorator to validate filter format."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Doc."""
        filters = [(k, v) for k, v in kwargs.items() if k not in KNOWN_PARAMS]

        if filters:
            for _filter in filters:
                operator = _filter[1].split(":")[0]

                if operator not in OPERATORS:
                    raise FilterFormatError

        return func(*args, **kwargs)

    return wrapped
