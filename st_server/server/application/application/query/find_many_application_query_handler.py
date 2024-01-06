from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.query_response import QueryResponse


class FindManyApplicationQueryHandler:
    def __init__(self, repository: ApplicationRepository) -> None:
        self._repository = repository

    def handle(self, query: FindManyApplicationQuery) -> QueryResponse:
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
