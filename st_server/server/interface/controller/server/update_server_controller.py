import configparser

from st_server.server.application.bus.command_bus import CommandBus
from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.infrastructure.bus.rabbitmq import RabbitMQMessageBus
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.shared.interface.controller import Controller

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


class UpdateServerController(Controller):
    """This is the entry point to update a Server.

    It will handle the command and dispatch it to the command bus
    to be handled by the command handler
    and then it will publish the domain events
    to be handled by the event handlers.
    """

    @staticmethod
    def handle(command: UpdateServerCommand):
        """Handle the given command."""
        repository = ServerRepositoryImpl(session.SessionLocal())
        message_bus = RabbitMQMessageBus(
            host=rabbitmq_host,
            port=rabbitmq_port,
            username=rabbitmq_user,
            password=rabbitmq_pass,
        )
        bus = CommandBus(repository=repository, message_bus=message_bus)
        bus.dispatch(command)
