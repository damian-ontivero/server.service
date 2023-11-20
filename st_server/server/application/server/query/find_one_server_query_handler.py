"""Query handler for finding one Server."""

from st_core.application.exception import NotFound

from st_server.server.application.server.dto.server import ServerDto
from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.domain.server.server_repository import ServerRepository


class FindOneServerQueryHandler:
    """Query handler for finding one Server."""

    def __init__(self, repository: ServerRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindOneServerQuery) -> ServerDto:
        """Handles a query."""
        server = self._repository.find_one(**query.to_dict())
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=query.id)
            )
        return ServerDto.from_entity(server)
