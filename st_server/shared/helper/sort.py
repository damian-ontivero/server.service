"""Validates _sort format."""

from functools import wraps

from st_server.shared.application.exception.exception import SortError


def validate_sort(func):
    """Decorator to validate _sort."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        _sort = kwargs.get("_sort", [])
        for _sort in _sort:
            if not isinstance(_sort, dict):
                raise SortError
            for key, value in _sort.items():
                if not isinstance(key, str):
                    raise SortError
                if not isinstance(value, str):
                    raise SortError
                if value not in ["asc", "desc"]:
                    raise SortError
        return func(*args, **kwargs)

    return wrapped
