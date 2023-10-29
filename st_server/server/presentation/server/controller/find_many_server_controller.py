import configparser

from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.application.server.query.find_many_server_query_handler import (
    FindManyServerQueryHandler,
)
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.server.presentation.server.dto.server import ServerDto
from st_server.shared.application.query_response import QueryResponse
from st_server.shared.presentation.controller import Controller

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


class FindManyServerController(Controller):
    """This is the entry point to find many Servers.

    It will handle the query and dispatch it to the query bus
    to be handled by the query handler.
    """

    @staticmethod
    def handle(query: FindManyServerQuery) -> QueryResponse:
        """Handle the given query."""
        repository = ServerRepositoryImpl(session.SessionLocal())
        handler = FindManyServerQueryHandler(repository=repository)
        result = handler.handle(query)
        return QueryResponse(
            total=result.total,
            limit=query.limit,
            offset=query.offset,
            items=[ServerDto.from_entity(server) for server in result.items],
        )
