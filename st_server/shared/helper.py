"""Helper functions."""

import datetime

from werkzeug.security import check_password_hash, generate_password_hash


def now() -> datetime.datetime:
    """Returns the current datetime.

    Returns:
        `datetime.datetime`: Current datetime.
    """
    return datetime.datetime.now()


def hash_password(password: str) -> str:
    """Hashes the provided password.

    Args:
        password (`str`): Password to be hashed.

    Returns:
        `str`: Hashed password.
    """
    return generate_password_hash(password=password, method="sha256")


def check_password(hashed_password: str, password: str) -> bool:
    """Checks if the provided password matches the hashed one.

    Args:
        hashed_password (`str`): Hashed password.
        password (`str`): Password to be checked.

    Returns:
        `bool`: `True` if the provided password matches the hashed one.
    """
    return check_password_hash(hashed_password, password)
