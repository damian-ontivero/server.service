"""Validates _filter format."""

from functools import wraps

from st_server.shared.application.exception.exception import FilterError

OPERATORS = ["eq", "gt", "ge", "lt", "le", "in", "btw", "lk"]


def validate_filter(func):
    """Decorator to validate _filter."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        _filter = kwargs.get("_filter", {})
        for key, value in _filter.items():
            if not isinstance(key, str):
                raise FilterError
            if not isinstance(value, dict):
                raise FilterError
            for op, val in value.items():
                if op not in OPERATORS:
                    raise FilterError
        _and_filter = kwargs.get("_and_filter", [])
        for _filter in _and_filter:
            for key, value in _filter.items():
                if not isinstance(key, str):
                    raise FilterError
                if not isinstance(value, dict):
                    raise FilterError
                for op, val in value.items():
                    if op not in OPERATORS:
                        raise FilterError
        _or_filter = kwargs.get("_or_filter", [])
        for _filter in _or_filter:
            for key, value in _filter.items():
                if not isinstance(key, str):
                    raise FilterError
                if not isinstance(value, dict):
                    raise FilterError
                for op, val in value.items():
                    if op not in OPERATORS:
                        raise FilterError
        return func(*args, **kwargs)

    return wrapped
