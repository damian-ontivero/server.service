"""Helper functions for time related operations."""

from datetime import datetime


def now() -> datetime:
    """Returns the current UTC datetime.

    Returns:
        `datetime`: Current UTC datetime.
    """
    return datetime.utcnow()
