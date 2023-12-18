from functools import wraps


def validate_pagination(func):
    """Validates the provided pagination attributes."""

    def validate_attribute(attr_name, attr_value, lower_bound):
        try:
            attr_int = int(attr_value)
            assert attr_int >= lower_bound
        except (ValueError, AssertionError):
            raise PaginationError(
                f"The {attr_name} number must be a non-negative integer value"
            )

    @wraps(func)
    def wrapped(*args, **kwargs):
        validate_attribute("limit", kwargs.get("limit", None), 0)
        validate_attribute("offset", kwargs.get("offset", None), 0)
        return func(*args, **kwargs)

    return wrapped


class PaginationError(Exception):
    """Raised when pagination fails."""

    pass
