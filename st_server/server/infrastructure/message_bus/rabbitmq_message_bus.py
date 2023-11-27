"""RabbitMQ message bus implementation."""

import json

import pika
from st_core.application.message_bus import MessageBus
from st_core.domain.domain_event import DomainEvent


class RabbitMQMessageBus(MessageBus):
    """RabbitMQ message bus implementation.

    Publishes domain events to RabbitMQ exchanges.
    """

    def __init__(
        self, host: str, port: int, username: str, password: str
    ) -> None:
        """Initializes the message bus."""
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=pika.PlainCredentials(username, password),
                virtual_host="server",
            )
        )
        self._channel = self._connection.channel()

    def publish(self, domain_event: DomainEvent) -> None:
        """Publishes a domain event."""
        aggregate, event = domain_event.__class__.__qualname__.split(".")
        routing_key = (
            ".".join([event.lower()[:-7], event.lower()[-7:]])
            if "Changed" in event
            else event.lower()
        )
        self._channel.basic_publish(
            exchange=aggregate.lower(),
            routing_key=routing_key,
            body=json.dumps(domain_event.__dict__, default=str),
        )
        self._connection.close()
