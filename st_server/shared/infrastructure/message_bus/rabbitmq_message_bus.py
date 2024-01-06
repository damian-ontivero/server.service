import json
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
        self._channel.basic_publish(
            exchange=self._get_exchange_name(domain_event),
            routing_key=self._get_routing_key(domain_event),
            body=json.dumps(domain_event.__dict__),
        )
        self._connection.close()

    def _get_aggregate_name(self, domain_event: DomainEvent) -> str:
        return domain_event.__class__.__qualname__.split(".")[0].lower()

    def _get_domain_event_name(self, domain_event: DomainEvent) -> str:
        return re.sub(
            r"(?<!^)(?=[A-Z])", ".", domain_event.__class__.__name__
        ).lower()

    def _get_exchange_name(self, domain_event: DomainEvent) -> str:
        return f"{self._get_aggregate_name(domain_event)}.domain_events"

    def _get_routing_key(self, domain_event: DomainEvent) -> str:
        aggregate_name = self._get_aggregate_name(domain_event)
        domain_event_name = self._get_domain_event_name(domain_event)
        return f"{aggregate_name}.{domain_event_name}"
