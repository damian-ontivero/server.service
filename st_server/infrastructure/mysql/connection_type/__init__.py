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
        class_=ConnectionType,
        local_table=ConnectionTypeDbModel.__table__,
    )

    mapper_registry.map_imperatively(
        class_=ConnectionTypeFull,
        local_table=ConnectionTypeDbModel.__table__,
    )

    mapper_registry.map_imperatively(
        class_=ConnectionTypeCreate,
        local_table=ConnectionTypeDbModel.__table__,
    )

    mapper_registry.map_imperatively(
        class_=ConnectionTypeUpdate,
        local_table=ConnectionTypeDbModel.__table__,
    )
