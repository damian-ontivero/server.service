from abc import ABCMeta, abstractmethod

from st_server.shared.domain.bus.query.query import Query
from st_server.shared.domain.bus.query.query_handler import QueryHandler


class QueryBus(metaclass=ABCMeta):
    @abstractmethod
    def register(self, query: Query, handler: QueryHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def ask(self, query: Query):
        raise NotImplementedError
