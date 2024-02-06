import json
import re

import pika

from st_server.shared.domain.bus.event.event_bus import EventBus
from st_server.shared.domain.domain_event import DomainEvent


class RabbitMQEventBus(EventBus):
    """
    RabbitMQMessageBus is a MessageBus implementation that uses RabbitMQ as
    message broker.

    Usage:
        with RabbitMQEventBus(
            host="localhost",
            port=5672,
            username="guest",
            password="guest",
        ) as event_bus:
            event_bus.publish(domain_event)
    """

    def __init__(
        self,
        domain: str,
        host: str,
        port: int,
        username: str,
        password: str,
    ) -> None:
        self._domain = domain
        self._host = host
        self._port = port
        self._credentials = pika.PlainCredentials(username, password)

    def _connect(self) -> None:
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._host,
                port=self._port,
                credentials=self._credentials,
            ),
        )
        self._channel = self._connection.channel()

    def _disconnect(self) -> None:
        if self._connection and not self._connection.is_closed:
            self._connection.close()

    def __enter__(self) -> "RabbitMQEventBus":
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._disconnect()

    def _get_aggregate_name(self, domain_event: DomainEvent) -> str:
        return domain_event.__class__.__qualname__.split(".")[0].lower()

    def _get_domain_event_name(self, domain_event: DomainEvent) -> str:
        return re.sub(
            r"(?<!^)(?=[A-Z])", ".", domain_event.__class__.__name__
        ).lower()

    def _get_routing_key(self, domain_event: DomainEvent) -> str:
        aggregate_name = self._get_aggregate_name(domain_event)
        domain_event_name = self._get_domain_event_name(domain_event)
        return f"{self._domain}.{aggregate_name}.{domain_event_name}"

    def publish(self, domain_event: DomainEvent) -> None:
        self._channel.basic_publish(
            exchange=f"{self._domain}.domain_events",
            routing_key=self._get_routing_key(domain_event),
            body=json.dumps(domain_event.__dict__),
            properties=pika.BasicProperties(content_type="application/json"),
        )
