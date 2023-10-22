import pytest

from st_server.server.application.server.dto.server import ServerReadDto
from st_server.server.application.server.query.find_many_query import (
    FindManyServerQuery,
)
from st_server.server.application.server.query.find_many_query_handler import (
    FindManyServerQueryHandler,
)
from st_server.server.application.server.query.find_one_query import (
    FindOneServerQuery,
)
from st_server.server.application.server.query.find_one_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.shared.application.exception import NotFound
from tests.util.factory.server_factory import ServerFactory


def test_find_many_ok():
    servers = ServerFactory.create_batch(5)

    query = FindManyServerQuery(
        filter={
            "id": {"in": ",".join([server.id.value for server in servers])}
        }
    )
    servers_found = FindManyServerQueryHandler().handle(query)

    assert servers_found.total == 5
    assert isinstance(servers_found.items[0], ServerReadDto)


def test_find_one_ok():
    server = ServerFactory()

    query = FindOneServerQuery(server.id.value)
    server_found = FindOneServerQueryHandler().handle(query)

    assert isinstance(server_found, ServerReadDto)
    assert server.id.value == server_found.id


def test_find_one_not_found():
    with pytest.raises(NotFound):
        query = FindOneServerQuery("1234")
        FindOneServerQueryHandler().handle(query)
