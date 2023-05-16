"""RabbitMQ message bus implementation."""

import json

import pika

from st_server.shared.domain_event import DomainEvent
from st_server.shared.message_bus import MessageBus


class RabbitMQMessageBus(MessageBus):
    """RabbitMQ message bus implementation."""

    def __init__(
        self, host: str, port: int, username: str, password: str
    ) -> None:
        """Initializes a new instance of the RabbitMQMessageBus class.

        Args:
            host (`str`): RabbitMQ host.
            port (`int`): RabbitMQ port.
            username (`str`): RabbitMQ username.
            password (`str`): RabbitMQ password.
        """
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=pika.PlainCredentials(username, password),
                virtual_host="support",
            )
        )

        self._channel = self._connection.channel()

    def publish(self, domain_events: list[DomainEvent]) -> None:
        """Publishes domain events.

        Args:
            domain_events (`list[DomainEvent]`): Domain events to publish.
        """
        cfg_ = {
            "user_updated": {
                "exchange": "user_exchange",
                "routing_key": "user.updated",
            },
            "user_created": {
                "exchange": "user_exchange",
                "routing_key": "user.created",
            },
            "user_discarded": {
                "exchange": "user_exchange",
                "routing_key": "user.discarded",
            },
            "role_updated": {
                "exchange": "role_exchange",
                "routing_key": "role.updated",
            },
            "role_created": {
                "exchange": "role_exchange",
                "routing_key": "role.created",
            },
            "role_discarded": {
                "exchange": "role_exchange",
                "routing_key": "role.discarded",
            },
        }

        for domain_event in domain_events:
            exchange_ = cfg_[domain_event.__dict__["type"]]["exchange"]
            routing_key_ = cfg_[domain_event.__dict__["type"]]["routing_key"]

            self._channel.basic_publish(
                exchange=exchange_,
                routing_key=routing_key_,
                body=json.dumps(domain_event.__dict__, default=str),
            )

        self._connection.close()
