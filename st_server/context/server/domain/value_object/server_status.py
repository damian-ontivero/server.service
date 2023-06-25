"""Value object that represents the status of the server."""

from st_server.shared.core.value_object import ValueObject


class ServerStatus(ValueObject):
    """Value object that represents the status of the server."""

    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"

    @classmethod
    def from_string(cls, value: str) -> "ServerStatus":
        if not value:
            raise ValueError("Server status cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Server status must be a string")
        if value not in [cls.RUNNING, cls.STOPPED, cls.ERROR, cls.UNKNOWN]:
            raise ValueError("Invalid server status")
        return cls(value=value)

    def __init__(self, value: str):
        self.__dict__["value"] = value

    @property
    def value(self) -> str:
        return self.__dict__["value"]
