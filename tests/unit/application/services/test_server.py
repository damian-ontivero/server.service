import pytest

from st_server.server.application.dtos.server import ServerReadDto
from st_server.shared.application.exceptions import NotFound
from tests.utils.factories.server_factory import ServerFactory


def test_find_many_ok(mock_server_service):
    servers = ServerFactory.create_batch(5)

    servers_found = mock_server_service.find_many(
        id="in:{}".format(",".join([server.id.value for server in servers]))
    )

    assert servers_found._total == 5
    assert isinstance(servers_found._items[0], ServerReadDto)


def test_find_one_ok(mock_server_service):
    server = ServerFactory()

    server_found = mock_server_service.find_one(id=server.id.value)

    assert isinstance(server_found, ServerReadDto)
    assert server.id.value == server_found.id


def test_find_one_not_found(mock_server_service):
    with pytest.raises(NotFound):
        mock_server_service.find_one(id="1234")


def test_add_one_ok(mock_server_service):
    server = ServerFactory.build()
    data = server.to_dict()

    server_created = mock_server_service.add_one(data=data)

    assert isinstance(server_created, ServerReadDto)
    assert server.name == server_created.name


def test_update_one_ok(mock_server_service):
    server = ServerFactory()
    server.name = "SuperTest"

    server_updated = mock_server_service.update_one(
        id=server.id.value, data=server.to_dict()
    )

    assert isinstance(server_updated, ServerReadDto)
    assert server_updated.name == server.name


def test_delete_one_ok(mock_server_service):
    server = ServerFactory()

    mock_server_service.delete_one(id=server.id.value)
