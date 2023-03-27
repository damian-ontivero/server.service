"""Exceptions and decorator to validate sort format."""

from functools import wraps


class SortFormatError(Exception):
    """Custom error that is raised when the sort format is incorrect."""

    def __str__(self) -> str:
        """Returns the string representation of an object."""
        return (
            "Incorrect sort format. Valid format: 'name:asc' or 'name:desc'."
        )


def validate_sort(func):
    """Decorator to validate sort format."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Doc."""
        sort = kwargs.get("sort", None)

        if sort:
            for sort_criteria in sort:
                criteria = sort_criteria.split(":")

                if len(criteria) != 2:
                    raise SortFormatError

                if criteria[1] not in ["asc", "desc"]:
                    raise SortFormatError

        return func(*args, **kwargs)

    return wrapped
