"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import registry, relationship

from st_server.server.domain.server.credential import Credential
from st_server.server.domain.server.server import Server
from st_server.server.infrastructure.persistence.mysql import db
from st_server.server.infrastructure.persistence.mysql.server.environment import (
    EnvironmentDbType,
)
from st_server.server.infrastructure.persistence.mysql.server.operating_system import (
    OperatingSystemDbType,
)
from st_server.server.infrastructure.persistence.mysql.server.server_status import (
    ServerStatusDbType,
)
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)

mapper_registry = registry()


class ServerDbModel(db.Base):
    """Server database model."""

    __tablename__ = "server"
    __table_args__ = (sa.PrimaryKeyConstraint("id"),)

    id = sa.Column(EntityIdDbType)
    name = sa.Column(sa.String(255), nullable=False)
    cpu = sa.Column(sa.String(255), nullable=True)
    ram = sa.Column(sa.String(255), nullable=True)
    hdd = sa.Column(sa.String(255), nullable=True)
    environment = sa.Column(EnvironmentDbType, nullable=False)
    operating_system = sa.Column(OperatingSystemDbType, nullable=False)
    status = sa.Column(ServerStatusDbType, nullable=True)
    discarded = sa.Column(sa.Boolean, nullable=False)


mapper_registry.map_imperatively(
    Server,
    ServerDbModel.__table__,
    properties={
        "_id": ServerDbModel.id,
        "_name": ServerDbModel.name,
        "_cpu": ServerDbModel.cpu,
        "_ram": ServerDbModel.ram,
        "_hdd": ServerDbModel.hdd,
        "_environment": ServerDbModel.environment,
        "_operating_system": ServerDbModel.operating_system,
        "_status": ServerDbModel.status,
        "_discarded": ServerDbModel.discarded,
        "_credentials": relationship(
            Credential, lazy="subquery", cascade="all, delete-orphan"
        ),
    },
)
