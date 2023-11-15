import pytest

from st_server.server.application.server.dto.server import ServerDto
from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.application.server.query.find_many_server_query_handler import (
    FindManyServerQueryHandler,
)
from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.application.server.query.find_one_server_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.shared.application.exception import NotFound
from tests.util.server.factory.server_factory import ServerFactory


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


def test_find_one_ok(mock_server_repository):
    server = ServerFactory()

    query = FindOneServerQuery(server.id.value)
    server_found = FindOneServerQueryHandler(mock_server_repository).handle(
        query
    )

    assert isinstance(server_found, ServerDto)
    assert server.id.value == server_found.id


def test_find_one_not_found(mock_server_repository):
    with pytest.raises(NotFound):
        query = FindOneServerQuery("1234")
        FindOneServerQueryHandler(mock_server_repository).handle(query)
