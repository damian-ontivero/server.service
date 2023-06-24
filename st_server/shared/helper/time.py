"""Helper functions for time related operations."""

from datetime import datetime


def now() -> datetime:
    return datetime.utcnow()
