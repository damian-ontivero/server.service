import configparser

from st_server.server.application.bus.command_bus import CommandBus
from st_server.server.infrastructure.bus.rabbitmq import RabbitMQMessageBus
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.shared.application.command import Command
from st_server.shared.interfaces.controller import Controller

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


class ServerController(Controller):
    """This is the entry point for all server commands."""

    @staticmethod
    def handle(command: Command):
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
