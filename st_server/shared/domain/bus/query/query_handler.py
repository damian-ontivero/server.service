from abc import ABCMeta, abstractmethod

from st_server.shared.domain.bus.query.query import Query


class QueryHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, query: Query):
        raise NotImplementedError
