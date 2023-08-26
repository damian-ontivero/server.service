"""Validates filter format."""

from functools import wraps

from st_server.shared.application.exceptions import FilterError

KNOWN_PARAMS = ["limit", "offset", "sort", "access_token"]
OPERATORS = ["eq", "gt", "ge", "lt", "le", "in", "btw", "lk"]


def validate_filter(func):
    """Decorator to validate filter."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        filters = [(k, v) for k, v in kwargs.items() if k not in KNOWN_PARAMS]
        if filters:
            for _filter in filters:
                operator = _filter[1].split(":")[0]
                if operator not in OPERATORS:
                    raise FilterError
        return func(*args, **kwargs)

    return wrapped
