"""Query handler for finding many Servers."""

from st_server.server.application.server.dto.server import ServerReadDto
from st_server.server.application.server.query.find_many_query import (
    FindManyServerQuery,
)
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.query_response import QueryResponse


class FindManyServerQueryHandler:
    """Query handler for finding many Servers."""

    def __init__(self, repository: ServerRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindManyServerQuery) -> ServerReadDto:
        """Handles a query."""
        applications = self._repository.find_many(**query.to_dict())
        total = applications.total
        return QueryResponse(
            total=total,
            limit=query.limit,
            offset=query.offset,
            items=[
                ServerReadDto.from_entity(application)
                for application in applications.items
            ],
        )
