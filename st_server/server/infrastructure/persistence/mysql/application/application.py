from sqlalchemy import Boolean, Column, String, Table

from st_server.server.domain.application.application import Application
from st_server.server.infrastructure.persistence.mysql import db
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)

application_table = Table(
    "application",
    db.metadata,
    Column("id", EntityIdDbType, primary_key=True),
    Column("name", String(255)),
    Column("version", String(255)),
    Column("architect", String(255)),
    Column("discarded", Boolean),
)


db.mapper_registry.map_imperatively(
    Application,
    application_table,
    properties={
        "_id": application_table.c.id,
        "_name": application_table.c.name,
        "_version": application_table.c.version,
        "_architect": application_table.c.architect,
        "_discarded": application_table.c.discarded,
    },
)
