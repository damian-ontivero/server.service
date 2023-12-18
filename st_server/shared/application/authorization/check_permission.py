import configparser
from functools import wraps

from st_server.shared.application.authorization.authorization_client import (
    AuthorizationClient,
)

config = configparser.ConfigParser()
config.read("st_server/config.ini")

HOST = config.get("grpc_auth", "host")
PORT = config.getint("grpc_auth", "port")


def check_permission(subject, obj, action):
    """Decorator to check permission for a user to perform an action on a resource."""

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            client = AuthorizationClient(host=HOST, port=PORT)
            allowed = client.check_permission(subject, obj, action)
            if not allowed:
                raise AuthorizationError(
                    f"Permission denied for {action} on {obj}"
                )
            return func(*args, **kwargs)

        return wrapped

    return decorator


class AuthorizationError(Exception):
    """Raised when a user fails to authorize."""

    pass
