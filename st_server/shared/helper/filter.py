"""Validates filter format."""

from functools import wraps

from st_server.shared.application.exception.exception import FilterError

OPERATORS = ["eq", "gt", "ge", "lt", "le", "in", "btw", "lk"]


def validate_filter(func):
    """Decorator to validate filter."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        filter = kwargs.get("filter", {})
        for key, value in filter.items():
            if not isinstance(key, str):
                raise FilterError
            if not isinstance(value, dict):
                raise FilterError
            for op, val in value.items():
                if op not in OPERATORS:
                    raise FilterError
        and_filter = kwargs.get("and_filter", [])
        for filter in and_filter:
            for key, value in filter.items():
                if not isinstance(key, str):
                    raise FilterError
                if not isinstance(value, dict):
                    raise FilterError
                for op, val in value.items():
                    if op not in OPERATORS:
                        raise FilterError
        or_filter = kwargs.get("or_filter", [])
        for filter in or_filter:
            for key, value in filter.items():
                if not isinstance(key, str):
                    raise FilterError
                if not isinstance(value, dict):
                    raise FilterError
                for op, val in value.items():
                    if op not in OPERATORS:
                        raise FilterError
        return func(*args, **kwargs)

    return wrapped
