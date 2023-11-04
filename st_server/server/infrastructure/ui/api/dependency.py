import configparser

from fastapi import Depends

from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.server.infrastructure.persistence.mysql.session import (
    SessionLocal,
)

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


def get_db_session():
    """Yields a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_message_bus():
    """Yields a message bus."""
    yield RabbitMQMessageBus(
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass,
    )
