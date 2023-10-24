import configparser

from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.application.server.query.find_one_server_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.shared.presentation.controller import Controller

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


class FindOneServerController(Controller):
    """This is the entry point to find one Server.

    It will handle the query and dispatch it to the query bus
    to be handled by the query handler.
    """

    @staticmethod
    def handle(query: FindOneServerQuery):
        """Handle the given query."""
        repository = ServerRepositoryImpl(session.SessionLocal())
        handler = FindOneServerQueryHandler(repository=repository)
        return handler.handle(query)
