"""Credential database model."""

from sqlalchemy import Boolean, Column, ForeignKey, String, Table

from st_server.server.domain.server.credential import Credential
from st_server.server.infrastructure.persistence.mysql import db
from st_server.server.infrastructure.persistence.mysql.server.connection_type import (
    ConnectionTypeDbType,
)
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)

credential_table = Table(
    "credential",
    db.metadata,
    Column("id", EntityIdDbType, primary_key=True),
    Column("server_id", ForeignKey("server.id")),
    Column("connection_type", ConnectionTypeDbType),
    Column("local_ip", String(255)),
    Column("local_port", String(255)),
    Column("public_ip", String(255)),
    Column("public_port", String(255)),
    Column("username", String(255)),
    Column("password", String(255)),
    Column("discarded", Boolean),
)


db.mapper_registry.map_imperatively(
    Credential,
    credential_table,
    properties={
        "_id": credential_table.c.id,
        "_server_id": credential_table.c.server_id,
        "_connection_type": credential_table.c.connection_type,
        "_local_ip": credential_table.c.local_ip,
        "_local_port": credential_table.c.local_port,
        "_public_ip": credential_table.c.public_ip,
        "_public_port": credential_table.c.public_port,
        "_username": credential_table.c.username,
        "_password": credential_table.c.password,
        "_discarded": credential_table.c.discarded,
    },
)
