from sqlalchemy.types import String, TypeDecorator

from st_server.server.domain.server.server_status import ServerStatus


class ServerStatusDbType(TypeDecorator):
    """
    Custom SQLAlchemy type for handling ServerStatus instances.

    This type converts ServerStatus objects to their string values for storage
    and retrieves them as ServerStatus instances.
    """

    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the value to be stored."""
        if value is not None:
            value = value.value
        return value

    def process_result_value(self, value, dialect):
        """Returns a value object instance from the stored value."""
        if value is not None:
            value = ServerStatus.from_text(value)
        return value
