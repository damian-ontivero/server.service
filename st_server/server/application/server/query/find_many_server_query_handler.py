from st_server.server.application.server.dto.server import ServerDto
from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.query_response import QueryResponse


class FindManyServerQueryHandler:
    def __init__(self, repository: ServerRepository) -> None:
        self._repository = repository

    def handle(self, query: FindManyServerQuery) -> QueryResponse:
        result = self._repository.find_many(**query.to_dict())
        return QueryResponse(
            total=result.total,
            limit=query.limit,
            offset=query.offset,
            items=[ServerDto.from_entity(server) for server in result.items],
        )
