from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.domain.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.query_response import QueryResponse
from st_server.shared.domain.bus.query.query_handler import QueryHandler


class FindManyApplicationQueryHandler(QueryHandler):
    def __init__(self, repository: ApplicationRepository) -> None:
        self._repository = repository

    def handle(self, query: FindManyApplicationQuery) -> QueryResponse:
        result = self._repository.find_many(
            limit=query.limit,
            offset=query.offset,
            filters=query.filter,
            and_filters=query.and_filter,
            or_filters=query.or_filter,
            sort=query.sort,
        )
        return QueryResponse(
            total=result.total,
            limit=query.limit,
            offset=query.offset,
            items=[
                ApplicationDto.from_entity(application)
                for application in result.items
            ],
        )
