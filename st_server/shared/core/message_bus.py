"""Abc for message bus."""

from abc import ABCMeta, abstractmethod

from st_server.shared.core.domain_event import DomainEvent


class MessageBus(metaclass=ABCMeta):
    @abstractmethod
    def publish(self, domain_events: list[DomainEvent]) -> None:
        raise NotImplementedError
