"""This is the infrastructure package for MySQL engine."""

from st_server.infrastructure.mysql import (
    application,
    connection_type,
    environment,
    operating_system,
    server,
)

application.start_mappers()
connection_type.start_mappers()
environment.start_mappers()
operating_system.start_mappers()
server.start_mappers()
