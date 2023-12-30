from sqlalchemy.types import String, TypeDecorator

from st_server.shared.domain.entity_id import EntityId


class EntityIdDbType(TypeDecorator):
    """
    Custom SQLAlchemy type for handling EntityId instances.

    This type converts EntityId objects to their string values for storage
    and retrieves them as EntityId instances.
    """

    impl = String(32)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the value to be stored."""
        if value is not None:
            value = value.value
        return value

    def process_result_value(self, value, dialect):
        """Returns a value object instance from the stored value."""
        if value is not None:
            value = EntityId.from_text(value)
        return value
