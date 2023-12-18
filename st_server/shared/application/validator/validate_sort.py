from functools import wraps


def validate_sort(func):
    """Validates the provided sort data."""

    def is_valid_sort(sort_item):
        if not isinstance(sort_item, dict):
            return False
        for key, value in sort_item.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
            if value not in ["asc", "desc"]:
                return False
        return True

    @wraps(func)
    def wrapped(*args, **kwargs):
        sorts = kwargs.get("sort", [])
        for sort_item in sorts:
            if not is_valid_sort(sort_item):
                raise SortError("Invalid sort format")
        return func(*args, **kwargs)

    return wrapped


class SortError(Exception):
    """Raised when sorting fails."""

    pass
