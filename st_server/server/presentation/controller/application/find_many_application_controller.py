import configparser

from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_application_query_handler import (
    FindManyApplicationQueryHandler,
)
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.application.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.shared.presentation.controller import Controller

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


class FindManyApplicationController(Controller):
    """This is the entry point to find many servers.

    It will handle the query and dispatch it to the query bus
    to be handled by the query handler.
    """

    @staticmethod
    def handle(query: FindManyApplicationQuery):
        """Handle the given query."""
        repository = ApplicationRepositoryImpl(session.SessionLocal())
        handler = FindManyApplicationQueryHandler(repository=repository)
        return handler.handle(query)
