import sqlalchemy as sa

from st_server.server.domain.server.connection_type import ConnectionType


class ConnectionTypeDbType(sa.types.TypeDecorator):
    """
    Custom SQLAlchemy type for handling ConnectionType instances.

    This type converts ConnectionType objects to their string values for storage
    and retrieves them as ConnectionType instances.
    """

    impl = sa.String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the ConnectionType value to be stored."""
        if value is None:
            return None
        if not isinstance(value, ConnectionType):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: ConnectionType"
            )
        return value.value

    def process_result_value(self, value, dialect):
        """Returns the stored value as a ConnectionType instance."""
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: str"
            )
        return ConnectionType.from_text(value)
