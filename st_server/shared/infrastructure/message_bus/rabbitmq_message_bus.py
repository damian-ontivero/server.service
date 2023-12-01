"""RabbitMQ message bus implementation."""

import json
import logging
import re

import pika

from st_server.shared.application.bus.message_bus import MessageBus
from st_server.shared.domain.domain_event import DomainEvent


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
            ),
        )
        self._channel = self._connection.channel()

    def publish(self, domain_event: DomainEvent) -> None:
        """Publishes a domain event."""
        self._channel.basic_publish(
            exchange=self._get_exchange_name(domain_event),
            routing_key=self._get_routing_key(domain_event),
            body=json.dumps(domain_event.__dict__),
        )
        self._connection.close()

    def _get_aggregate_name(self, domain_event: DomainEvent) -> str:
        """Gets the aggregate name for a domain event."""
        return domain_event.__class__.__qualname__.split(".")[0].lower()

    def _get_domain_event_name(self, domain_event: DomainEvent) -> str:
        """Gets the domain event name for a domain event."""
        return re.sub(
            r"(?<!^)(?=[A-Z])", ".", domain_event.__class__.__name__
        ).lower()

    def _get_exchange_name(self, domain_event: DomainEvent) -> str:
        """Gets the exchange name for a domain event."""
        return f"{self._get_aggregate_name(domain_event)}.domain_events"

    def _get_routing_key(self, domain_event: DomainEvent) -> str:
        """Gets the routing key for a domain event."""
        aggregate_name = self._get_aggregate_name(domain_event)
        domain_event_name = self._get_domain_event_name(domain_event)
        return f"{aggregate_name}.{domain_event_name}"
