import sqlalchemy as sa

from st_server.server.domain.server.operating_system import OperatingSystem


class OperatingSystemDbType(sa.types.TypeDecorator):
    """
    Custom SQLAlchemy type for handling OperatingSystem instances.

    This type converts OperatingSystem objects to their string values for storage
    and retrieves them as OperatingSystem instances.
    """

    impl = sa.JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the OperatingSystem value to be stored."""
        if value is None:
            return None
        if not isinstance(value, OperatingSystem):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: OperatingSystem"
            )
        return value.__dict__

    def process_result_value(self, value, dialect):
        """Returns the stored value as an OperatingSystem instance."""
        if value is None:
            return None
        if not isinstance(value, dict):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: dict"
            )
        return OperatingSystem.from_data(value)
