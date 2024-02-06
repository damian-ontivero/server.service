from st_server.server.server.application.dto.server import ServerDto
from st_server.server.server.application.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.server.domain.server_repository import ServerRepository
from st_server.shared.application.exception import NotFound
from st_server.shared.domain.bus.query.query_handler import QueryHandler


class FindOneServerQueryHandler(QueryHandler):
    def __init__(self, repository: ServerRepository) -> None:
        self._repository = repository

    def handle(self, query: FindOneServerQuery) -> ServerDto:
        server = self._repository.find_by_id(query.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=query.id)
            )
        return ServerDto.from_entity(server)
