import pytest

from st_server.server.application.server.dto.server import ServerReadDto
from st_server.shared.application.exception import NotFound
from tests.util.factory.server_factory import ServerFactory


def test_find_many_ok(mock_server_query):
    servers = ServerFactory.create_batch(5)

    servers_found = mock_server_query.find_many(
        filter={
            "id": {"in": ",".join([server.id.value for server in servers])}
        }
    )

    assert servers_found.total == 5
    assert isinstance(servers_found.items[0], ServerReadDto)


def test_find_one_ok(mock_server_query):
    server = ServerFactory()

    server_found = mock_server_query.find_one(server.id.value)

    assert isinstance(server_found, ServerReadDto)
    assert server.id.value == server_found.id


def test_find_one_not_found(mock_server_query):
    with pytest.raises(NotFound):
        mock_server_query.find_one("1234")
