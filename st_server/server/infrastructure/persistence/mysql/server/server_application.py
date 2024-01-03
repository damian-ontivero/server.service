"""ServerApplication database model."""

from sqlalchemy import Column, ForeignKey, String, Table

from st_server.server.domain.server.server_application import ServerApplication
from st_server.server.infrastructure.persistence.mysql import db

server_application_table = Table(
    "server_application",
    db.metadata,
    Column("server_id", ForeignKey("server.id"), primary_key=True),
    Column("application_id", ForeignKey("application.id"), primary_key=True),
    Column("install_dir", String(255)),
    Column("log_dir", String(255)),
)


db.mapper_registry.map_imperatively(
    ServerApplication,
    server_application_table,
    properties={
        "_server_id": server_application_table.c.server_id,
        "_application_id": server_application_table.c.application_id,
        "_install_dir": server_application_table.c.install_dir,
        "_log_dir": server_application_table.c.log_dir,
    },
)
