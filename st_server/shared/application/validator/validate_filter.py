from functools import wraps

OPERATORS = ["eq", "gt", "ge", "lt", "le", "in", "btw", "lk"]


def validate_filter(func):
    """Validates the provided filter data."""

    def validate_individual_filter(filter_data):
        for key, value in filter_data.items():
            if not isinstance(key, str) or not isinstance(value, dict):
                raise FilterError("Invalid filter format")
            for op in value.keys():
                if op not in OPERATORS:
                    raise FilterError(f"Invalid operator: {op}")

    @wraps(func)
    def wrapped(*args, **kwargs):
        filters = [
            kwargs.get("filter", {}),
            *kwargs.get("and_filter", []),
            *kwargs.get("or_filter", []),
        ]
        for filter_data in filters:
            validate_individual_filter(filter_data)
        return func(*args, **kwargs)

    return wrapped


class FilterError(Exception):
    """Raised when filtering fails."""

    pass
