"""Doc."""

from sqlalchemy import MetaData
from sqlalchemy.orm import registry

from st_server.domain.environment import (
    Environment,
    EnvironmentCreate,
    EnvironmentFull,
    EnvironmentUpdate,
)

from .environment import EnvironmentDbModel

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mappers():
    """Start the SQLAlchemy mappers."""
    # This is needed to ensure the mappers are started before any
    # configuration and class creation operations are called.
    # Otherwise, the mappers will not be available, and the
    # configuration will fail.

    mapper_registry.map_imperatively(Environment, EnvironmentDbModel.__table__)
    mapper_registry.map_imperatively(
        EnvironmentFull, EnvironmentDbModel.__table__
    )
    mapper_registry.map_imperatively(
        EnvironmentCreate, EnvironmentDbModel.__table__
    )
    mapper_registry.map_imperatively(
        EnvironmentUpdate, EnvironmentDbModel.__table__
    )


start_mappers()
