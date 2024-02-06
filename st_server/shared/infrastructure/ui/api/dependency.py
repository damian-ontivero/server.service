import configparser

from st_server.server.application.infrastructure.persistence.mysql.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.server.server.infrastructure.persistence.mysql.server_repository import (
    ServerRepositoryImpl,
)
from st_server.shared.infrastructure.bus.event.rabbitmq_event_bus import (
    RabbitMQEventBus,
)
from st_server.shared.infrastructure.persistence.mysql import db

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


def get_server_repository():
    return ServerRepositoryImpl(db.SessionLocal())


def get_application_repository():
    return ApplicationRepositoryImpl(db.SessionLocal())


def get_rabbitmq_event_bus():
    return RabbitMQEventBus(
        domain="server",
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass,
    )
