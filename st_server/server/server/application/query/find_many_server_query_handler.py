from st_server.server.server.application.dto.server import ServerDto
from st_server.server.server.application.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.server.domain.server_repository import ServerRepository
from st_server.shared.application.query_response import QueryResponse
from st_server.shared.domain.bus.query.query_handler import QueryHandler


class FindManyServerQueryHandler(QueryHandler):
    def __init__(self, repository: ServerRepository) -> None:
        self._repository = repository

    def handle(self, query: FindManyServerQuery) -> QueryResponse:
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
            items=[ServerDto.from_entity(server) for server in result.items],
        )
