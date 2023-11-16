"""Authentication query."""

import configparser
from functools import wraps

import jwt

config = configparser.ConfigParser()
config.read("st_support/config.ini")

TOKEN_SECRET = config.get("access_token", "secret")
TOKEN_ALGO = config.get("access_token", "algorithm")
TOKEN_EXPIRE = config.getint("access_token", "expire_seconds")


def validate_access_token(func):
    """Decorator to validate access token."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        access_token = kwargs.get("access_token", None)
        jwt.decode(
            jwt=access_token,
            key=TOKEN_SECRET,
            algorithms=TOKEN_ALGO,
        )
        return func(*args, **kwargs)

    return wrapped
