"""Helper functions for time related operations."""

from datetime import datetime


def now() -> datetime:
    """Returns the current datetime.

    Returns:
        `datetime`: Current datetime.
    """
    return datetime.now()
