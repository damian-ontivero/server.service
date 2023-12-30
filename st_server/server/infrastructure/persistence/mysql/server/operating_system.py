from sqlalchemy.types import JSON, TypeDecorator

from st_server.server.domain.server.operating_system import OperatingSystem


class OperatingSystemDbType(TypeDecorator):
    """
    Custom SQLAlchemy type for handling OperatingSystem instances.

    This type converts OperatingSystem objects to their string values for storage
    and retrieves them as OperatingSystem instances.
    """

    impl = JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the value to be stored."""
        if value is not None:
            value = value.__dict__
        return value

    def process_result_value(self, value, dialect):
        """Returns a value object instance from the stored value."""
        if value is not None:
            value = OperatingSystem.from_data(value)
        return value
