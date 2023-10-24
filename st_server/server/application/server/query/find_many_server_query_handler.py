"""Query handler for finding many Servers."""

from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.domain.repository_response import RepositoryResponse


class FindManyServerQueryHandler:
    """Query handler for finding many Servers."""

    def __init__(self, repository: ServerRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindManyServerQuery) -> RepositoryResponse:
        """Handles a query."""
        return self._repository.find_many(**query.to_dict())
