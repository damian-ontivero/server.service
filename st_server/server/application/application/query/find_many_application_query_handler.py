"""Query handler for finding many Applications."""

from st_core.application.query_response import QueryResponse
from st_core.domain.repository_response import RepositoryResponse

from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)


class FindManyApplicationQueryHandler:
    """Query handler for finding many Applications."""

    def __init__(self, repository: ApplicationRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindManyApplicationQuery) -> RepositoryResponse:
        """Handles a query."""
        result = self._repository.find_many(**query.to_dict())
        return QueryResponse(
            total=result.total,
            limit=query.limit,
            offset=query.offset,
            items=[
                ApplicationDto.from_entity(application)
                for application in result.items
            ],
        )
