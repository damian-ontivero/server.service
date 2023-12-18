import sqlalchemy as sa

from st_server.shared.domain.entity_id import EntityId


class EntityIdDbType(sa.types.TypeDecorator):
    """
    Custom SQLAlchemy type for handling EntityId instances.

    This type converts EntityId objects to their string values for storage
    and retrieves them as EntityId instances.
    """

    impl = sa.String(32)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Returns the EntityId value to be stored."""
        if value is None:
            return None
        if not isinstance(value, EntityId):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: EntityId"
            )
        return value.value

    def process_result_value(self, value, dialect):
        """Returns the stored value as an EntityId instance."""
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(
                f"Invalid value type: {type(value)}. Expected type: str"
            )
        return EntityId.from_text(value)
