import configparser
from functools import wraps

import jwt

config = configparser.ConfigParser()
config.read("st_server/config.ini")

TOKEN_SECRET = config.get("access_token", "secret")
TOKEN_ALGO = config.get("access_token", "algorithm")
TOKEN_EXPIRE = config.getint("access_token", "expire_seconds")


def validate_access_token(func):
    """Validates the provided access token using JWT decoding."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        access_token = kwargs.get("access_token", None)
        try:
            # Attempt to decode the access token
            jwt.decode(
                jwt=access_token,
                key=TOKEN_SECRET,
                algorithms=TOKEN_ALGO,
            )
        except jwt.ExpiredSignatureError:
            # Handle an expired token
            # You can add custom handling or raise an appropriate exception
            raise ValueError("Access token has expired")
        except jwt.InvalidTokenError:
            # Handle an invalid token
            # You can add custom handling or raise an appropriate exception
            raise ValueError("Invalid access token")

        # If token is valid, execute the wrapped function
        return func(*args, **kwargs)

    return wrapped
