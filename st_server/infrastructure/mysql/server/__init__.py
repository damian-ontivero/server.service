"""Doc."""

from sqlalchemy import MetaData
from sqlalchemy.orm import registry, relationship

from st_server.domain.application import Application, ApplicationFull
from st_server.domain.connection_type import ConnectionType, ConnectionTypeFull
from st_server.domain.environment import Environment, EnvironmentFull
from st_server.domain.operating_system import (
    OperatingSystem,
    OperatingSystemFull,
)
from st_server.domain.server import (
    Credential,
    CredentialCreate,
    CredentialFull,
    CredentialSimple,
    CredentialUpdate,
    Server,
    ServerApplication,
    ServerApplicationFull,
    ServerCreate,
    ServerFull,
    ServerSimple,
    ServerUpdate,
)

from .credential import CredentialDbModel
from .server import ServerDbModel
from .server_application import ServerApplicationDbModel

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mappers():
    """Start the SQLAlchemy mappers."""
    # This is needed to ensure the mappers are started before any
    # configuration and class creation operations are called.
    # Otherwise, the mappers will not be available, and the
    # configuration will fail.

    # Server
    mapper_registry.map_imperatively(
        Server,
        ServerDbModel.__table__,
        properties={
            "environment": relationship(
                Environment, lazy="joined", viewonly=True
            ),
            "operating_system": relationship(
                OperatingSystem, lazy="joined", viewonly=True
            ),
            "credentials": relationship(
                Credential, lazy="joined", viewonly=True
            ),
            "applications": relationship(
                ServerApplication, lazy="joined", viewonly=True
            ),
        },
    )
    mapper_registry.map_imperatively(
        ServerFull,
        ServerDbModel.__table__,
        properties={
            "environment": relationship(
                EnvironmentFull, lazy="joined", viewonly=True
            ),
            "operating_system": relationship(
                OperatingSystemFull, lazy="joined", viewonly=True
            ),
            "credentials": relationship(
                CredentialFull, lazy="joined", viewonly=True
            ),
            "applications": relationship(
                ServerApplicationFull, lazy="joined", viewonly=True
            ),
        },
    )
    mapper_registry.map_imperatively(ServerSimple, ServerDbModel.__table__)
    mapper_registry.map_imperatively(ServerCreate, ServerDbModel.__table__)
    mapper_registry.map_imperatively(ServerUpdate, ServerDbModel.__table__)

    # ServerApplication
    mapper_registry.map_imperatively(
        ServerApplication,
        ServerApplicationDbModel.__table__,
        properties={"application": relationship(Application, lazy="joined")},
    )
    mapper_registry.map_imperatively(
        ServerApplicationFull,
        ServerApplicationDbModel.__table__,
        properties={
            "application": relationship(ApplicationFull, lazy="joined")
        },
    )

    # Credential
    mapper_registry.map_imperatively(
        Credential,
        CredentialDbModel.__table__,
        properties={
            "connection_type": relationship(
                ConnectionType, lazy="joined", viewonly=True
            )
        },
    )
    mapper_registry.map_imperatively(
        CredentialFull,
        CredentialDbModel.__table__,
        properties={
            "connection_type": relationship(
                ConnectionTypeFull, lazy="joined", viewonly=True
            )
        },
    )
    mapper_registry.map_imperatively(
        CredentialSimple, CredentialDbModel.__table__
    )
    mapper_registry.map_imperatively(
        CredentialCreate, CredentialDbModel.__table__
    )
    mapper_registry.map_imperatively(
        CredentialUpdate, CredentialDbModel.__table__
    )


start_mappers()
