"""Doc."""

from sqlalchemy import MetaData
from sqlalchemy.orm import registry

from st_server.domain.connection_type import (
    ConnectionType,
    ConnectionTypeCreate,
    ConnectionTypeFull,
    ConnectionTypeUpdate,
)

from .connection_type import ConnectionTypeDbModel

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mappers():
    """Start the SQLAlchemy mappers."""
    # This is needed to ensure the mappers are started before any
    # configuration and class creation operations are called.
    # Otherwise, the mappers will not be available, and the
    # configuration will fail.

    mapper_registry.map_imperatively(
        ConnectionType, ConnectionTypeDbModel.__table__
    )
    mapper_registry.map_imperatively(
        ConnectionTypeFull, ConnectionTypeDbModel.__table__
    )
    mapper_registry.map_imperatively(
        ConnectionTypeCreate, ConnectionTypeDbModel.__table__
    )
    mapper_registry.map_imperatively(
        ConnectionTypeUpdate, ConnectionTypeDbModel.__table__
    )


start_mappers()
