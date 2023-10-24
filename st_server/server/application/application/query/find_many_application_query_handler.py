"""Query handler for finding many Applications."""

from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.domain.repository_response import RepositoryResponse


class FindManyApplicationQueryHandler:
    """Query handler for finding many Applications."""

    def __init__(self, repository: ApplicationRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindManyApplicationQuery) -> RepositoryResponse:
        """Handles a query."""
        return self._repository.find_many(**query.to_dict())
