from abc import ABCMeta, abstractmethod

from st_server.shared.domain.domain_event import DomainEvent


class EventBus(metaclass=ABCMeta):
    @abstractmethod
    def publish(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError
