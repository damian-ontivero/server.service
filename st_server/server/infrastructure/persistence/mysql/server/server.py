"""Server database model."""

from sqlalchemy import Boolean, Column, String, Table
from sqlalchemy.orm import relationship

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

server_table = Table(
    "server",
    db.metadata,
    Column("id", EntityIdDbType, primary_key=True),
    Column("name", String(255)),
    Column("cpu", String(255)),
    Column("ram", String(255)),
    Column("hdd", String(255)),
    Column("environment", EnvironmentDbType),
    Column("operating_system", OperatingSystemDbType),
    Column("status", ServerStatusDbType),
    Column("discarded", Boolean),
)


db.mapper_registry.map_imperatively(
    Server,
    server_table,
    properties={
        "_id": server_table.c.id,
        "_name": server_table.c.name,
        "_cpu": server_table.c.cpu,
        "_ram": server_table.c.ram,
        "_hdd": server_table.c.hdd,
        "_environment": server_table.c.environment,
        "_operating_system": server_table.c.operating_system,
        "_status": server_table.c.status,
        "_discarded": server_table.c.discarded,
        "_credentials": relationship(
            Credential, lazy="subquery", cascade="all, delete-orphan"
        ),
    },
)
