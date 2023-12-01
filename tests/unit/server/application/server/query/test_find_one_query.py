"""Test for find many server query."""

import pytest

from st_server.server.application.server.dto.server import ServerDto
from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.application.server.query.find_one_server_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.shared.application.exception import NotFound
from tests.util.server.domain.server.server_factory import ServerFactory


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
