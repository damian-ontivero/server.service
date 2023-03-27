"""Doc."""

from sqlalchemy import MetaData
from sqlalchemy.orm import registry

from st_server.domain.operating_system import (
    OperatingSystem,
    OperatingSystemCreate,
    OperatingSystemFull,
    OperatingSystemUpdate,
)

from .operating_system import OperatingSystemDbModel

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mappers():
    """Start the SQLAlchemy mappers."""
    # This is needed to ensure the mappers are started before any
    # configuration and class creation operations are called.
    # Otherwise, the mappers will not be available, and the
    # configuration will fail.

    mapper_registry.map_imperatively(
        OperatingSystem, OperatingSystemDbModel.__table__
    )
    mapper_registry.map_imperatively(
        OperatingSystemFull, OperatingSystemDbModel.__table__
    )
    mapper_registry.map_imperatively(
        OperatingSystemCreate, OperatingSystemDbModel.__table__
    )
    mapper_registry.map_imperatively(
        OperatingSystemUpdate, OperatingSystemDbModel.__table__
    )


start_mappers()
