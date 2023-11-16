"""Dependencies."""

import configparser

from st_server.server.application.command_bus.command_bus import CommandBus
from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.persistence.mysql.db import SessionLocal

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


def get_mysql_session():
    """Yields a mysql session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_command_bus():
    """Yields a command bus."""
    return CommandBus()


def get_rabbitmq_message_bus():
    """Yields a message bus."""
    return RabbitMQMessageBus(
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass,
    )
