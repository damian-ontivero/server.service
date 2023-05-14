"""Helper functions for time and date handling."""

import datetime

import pytz

TIME_ZONE = pytz.timezone("Europe/Madrid")


def now() -> datetime.datetime:
    """Returns the current datetime.

    Returns:
        `datetime.datetime`: Current datetime.
    """
    return datetime.datetime.now(TIME_ZONE)
