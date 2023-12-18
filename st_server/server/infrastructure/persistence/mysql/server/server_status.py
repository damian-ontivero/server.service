import sqlalchemy as sa

from st_server.server.domain.server.server_status import ServerStatus


class ServerStatusDbType(sa.types.TypeDecorator):
    """
    Custom SQLAlchemy type for handling ServerStatus instances.

    This type converts ServerStatus objects to their string values for storage
    and retrieves them as ServerStatus instances.
    """

    impl = sa.String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the ServerStatus value to be stored."""
        if value is None:
            return None
        if not isinstance(value, ServerStatus):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: ServerStatus"
            )
        return value.value

    def process_result_value(self, value, dialect):
        """Returns the stored value as a ServerStatus instance."""
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: str"
            )
        return ServerStatus.from_text(value)
