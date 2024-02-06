from st_server.server.server.application.dto.server import ServerDto
from st_server.server.server.application.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.server.application.query.find_many_server_query_handler import (
    FindManyServerQueryHandler,
)
from tests.util.server.domain.server.server_factory import ServerFactory


def test_find_many_ok(mock_server_repository):
    servers = ServerFactory.create_batch(5)

    query = FindManyServerQuery(
        filter={
            "id": {"in": ",".join([server.id.value for server in servers])}
        }
    )
    servers_found = FindManyServerQueryHandler(mock_server_repository).handle(
        query
    )

    assert servers_found.total == 5
    assert isinstance(servers_found.items[0], ServerDto)
