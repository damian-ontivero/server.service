"""Exceptions and decorator to validate sort format."""

from functools import wraps

from st_server.shared.core.exception import SortError


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
                    raise SortError

                if criteria[1] not in ["asc", "desc"]:
                    raise SortError

        return func(*args, **kwargs)

    return wrapped
