import configparser
from functools import wraps

from st_server.shared.application.authorization.authorization_client import (
    AuthorizationClient,
)

config = configparser.ConfigParser()
config.read("st_server/config.ini")

HOST = config.get("grpc_auth", "host")
PORT = config.get("grpc_auth", "port")


def check_permission(func):
    """Decorator to check permission for a user
    to perform an action on a resource.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        # module = function.__module__
        # domain = os.path.splitext(module)[0]
        # resource = f"{domain}.{function.__qualname__.split('.')[0]}"
        # action = function.__name__

        client = AuthorizationClient(host=HOST, port=PORT)
        allowed = client.check_permission(
            subject="user",
            object="resource",
            action="read",
        )
        if not allowed:
            raise AuthorizationError("Permission denied")
        return func(*args, **kwargs)

    return wrapped


class AuthorizationError(Exception):
    """Raised when a user fails to authorize."""

    pass
