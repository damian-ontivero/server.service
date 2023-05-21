"""RabbitMQ message bus implementation."""

import json

import pika

from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.message_bus import MessageBus


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
        for domain_event in domain_events:
            qualname = domain_event.__class__.__qualname__

            self._channel.basic_publish(
                exchange=qualname.split(".")[0].lower(),
                routing_key=domain_event.__dict__["type_"],
                body=json.dumps(domain_event.__dict__, default=str),
            )

        self._connection.close()
