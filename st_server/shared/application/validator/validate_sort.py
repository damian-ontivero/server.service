"""Validates sort format."""

from functools import wraps


def validate_sort(func):
    """Decorator to validate sort."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        sort = kwargs.get("sort", [])
        for sort in sort:
            if not isinstance(sort, dict):
                raise SortError
            for key, value in sort.items():
                if not isinstance(key, str):
                    raise SortError
                if not isinstance(value, str):
                    raise SortError
                if value not in ["asc", "desc"]:
                    raise SortError
        return func(*args, **kwargs)

    return wrapped


class SortError(Exception):
    """Raised when sorting fails."""

    pass
