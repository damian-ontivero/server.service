import sqlalchemy as sa

from st_server.server.domain.server.environment import Environment


class EnvironmentDbType(sa.types.TypeDecorator):
    """
    Custom SQLAlchemy type for handling Environment instances.

    This type converts Environment objects to their string values for storage
    and retrieves them as Environment instances.
    """

    impl = sa.String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the Environment value to be stored."""
        if value is None:
            return None
        if not isinstance(value, Environment):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: Environment"
            )
        return value.value

    def process_result_value(self, value, dialect):
        """Returns the stored value as an Environment instance."""
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: str"
            )
        return Environment.from_text(value)
