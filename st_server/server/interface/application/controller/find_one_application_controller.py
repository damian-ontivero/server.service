import configparser

from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.application.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.server.interface.application.dto.application import (
    ApplicationDto,
)
from st_server.shared.interface.controller import Controller

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


class FindOneApplicationController(Controller):
    """This is the entry point to find one server.

    It will handle the query and dispatch it to the query bus
    to be handled by the query handler.
    """

    @staticmethod
    def handle(query: FindOneApplicationQuery):
        """Handle the given query."""
        repository = ApplicationRepositoryImpl(session.SessionLocal())
        handler = FindOneApplicationQueryHandler(repository)
        result = handler.handle(query)
        return ApplicationDto.from_entity(result)