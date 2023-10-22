"""Query handler for finding one Application."""

from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.server.application.application.query.find_one_query import (
    FindOneApplicationQuery,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.exception import NotFound


class FindOneApplicationQueryHandler:
    """Query handler for finding one Application."""

    def __init__(self, repository: ApplicationRepository) -> None:
        """Initialize the handler."""
        self._repository = repository

    def handle(self, query: FindOneApplicationQuery) -> ApplicationReadDto:
        """Handles a query."""
        application = self._repository.find_one(**query.to_dict())
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=id)
            )
        return ApplicationReadDto.from_entity(application)
