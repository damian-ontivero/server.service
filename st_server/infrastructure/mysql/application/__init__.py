"""Doc."""

from sqlalchemy import MetaData
from sqlalchemy.orm import registry

from st_server.domain.application.application import (
    Application,
    ApplicationCreate,
    ApplicationFull,
    ApplicationUpdate,
)

from .application import ApplicationDbModel

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mappers():
    """Start the SQLAlchemy mappers."""
    # This is needed to ensure the mappers are started before any
    # configuration and class creation operations are called.
    # Otherwise, the mappers will not be available, and the
    # configuration will fail.

    mapper_registry.map_imperatively(
        class_=Application,
        local_table=ApplicationDbModel.__table__,
    )

    mapper_registry.map_imperatively(
        class_=ApplicationFull,
        local_table=ApplicationDbModel.__table__,
    )

    mapper_registry.map_imperatively(
        class_=ApplicationCreate,
        local_table=ApplicationDbModel.__table__,
    )

    mapper_registry.map_imperatively(
        class_=ApplicationUpdate,
        local_table=ApplicationDbModel.__table__,
    )
