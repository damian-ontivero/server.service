"""Query handler for finding many Applications."""

from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.server.application.application.query.find_many_query import (
    FindManyApplicationQuery,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.query_response import QueryResponse


class FindManyApplicationQueryHandler:
    """Query handler for finding many Applications."""

    def __init__(self, repository: ApplicationRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindManyApplicationQuery) -> ApplicationReadDto:
        """Handles a query."""
        applications = self._repository.find_many(**query.to_dict())
        total = applications.total
        return QueryResponse(
            total=total,
            limit=query.limit,
            offset=query.offset,
            items=[
                ApplicationReadDto.from_entity(application)
                for application in applications.items
            ],
        )
