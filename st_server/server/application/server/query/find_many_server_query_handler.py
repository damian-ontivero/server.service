"""Query handler for finding many Servers."""

from st_server.shared.application.query_response import QueryResponse

from st_server.server.application.server.dto.server import ServerDto
from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.domain.server.server_repository import ServerRepository


class FindManyServerQueryHandler:
    """Query handler for finding many Servers."""

    def __init__(self, repository: ServerRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindManyServerQuery) -> QueryResponse:
        """Handles a query."""
        result = self._repository.find_many(**query.to_dict())
        return QueryResponse(
            total=result.total,
            limit=query.limit,
            offset=query.offset,
            items=[ServerDto.from_entity(server) for server in result.items],
        )
