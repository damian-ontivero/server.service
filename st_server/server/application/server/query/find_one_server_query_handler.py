"""Query handler for finding one Server."""

from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.domain.server.server import Server
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.exception import NotFound


class FindOneServerQueryHandler:
    """Query handler for finding one Server."""

    def __init__(self, repository: ServerRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindOneServerQuery) -> Server:
        """Handles a query."""
        server = self._repository.find_one(**query.to_dict())
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=query.id)
            )
        return server
