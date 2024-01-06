import configparser

from st_server.server.infrastructure.persistence.mysql import db
from st_server.shared.application.bus.command_bus import CommandBus
from st_server.shared.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


def get_mysql_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_command_bus():
    return CommandBus()


def get_rabbitmq_message_bus():
    return RabbitMQMessageBus(
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass,
    )
