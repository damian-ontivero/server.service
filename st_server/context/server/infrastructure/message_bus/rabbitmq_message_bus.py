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
            """
            Exchange:
                Aggregate root which published the event.
                    User.FirstNameChanged -> user

            Routing key:
                If the domain event is a property changed event:
                    User.FirstNameChanged -> firstname.changed

                If the domain event is not a property changed event:
                    User.Created -> created

            Body:
                User.FirstNameChanged -> {
                    "occurred_on": "2023-06-05 22:06:19.683588",
                    "aggregate_id": "3af25ebdf13a421080910ef6b4b8b474",
                    "old_value": "John",
                    "new_value": "Johny"
                }
            """
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
