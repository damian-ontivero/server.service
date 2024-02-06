from typing import Dict

from st_server.shared.domain.bus.query.query import Query
from st_server.shared.domain.bus.query.query_handler import QueryHandler


class InMemoryQueryBus:
    _instance = None

    def __new__(cls) -> "InMemoryQueryBus":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers: Dict[Query, QueryHandler] = {}
        return cls._instance

    def register(self, query: Query, handler: QueryHandler) -> None:
        if not issubclass(query, Query):
            raise TypeError(
                f"Invalid query type: {query.__class__.__name__}. Expected type: Query"
            )
        if not isinstance(handler, QueryHandler):
            raise TypeError(
                f"Invalid handler type: {handler.__class__.__name__}. Expected type: QueryHandler"
            )
        if type(query) in self._handlers:
            raise NotImplementedError(
                f"Query {type(query)} is already registered"
            )
        self._handlers[query] = handler

    def ask(self, query: Query):
        if not isinstance(query, Query):
            raise TypeError(
                f"Invalid query type: {query.__class__.__name__}. Expected type: Query"
            )
        if type(query) not in self._handlers:
            raise NotImplementedError(
                f"No registered handler found for query: {query.__class__.__name__}"
            )
        handler = self._handlers[type(query)]
        return handler.handle(query)
