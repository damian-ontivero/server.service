"""Test for find one application query."""

import pytest

from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.shared.application.exception import NotFound
from tests.util.server.domain.application.application_factory import (
    ApplicationFactory,
)


def test_find_one_ok(mock_application_repository):
    application = ApplicationFactory()

    query = FindOneApplicationQuery(application.id.value)
    application_found = FindOneApplicationQueryHandler(
        mock_application_repository
    ).handle(query)

    assert isinstance(application_found, ApplicationDto)
    assert application.id.value == application_found.id


def test_find_one_not_found(mock_application_repository):
    with pytest.raises(NotFound):
        query = FindOneApplicationQuery("1234")
        FindOneApplicationQueryHandler(mock_application_repository).handle(
            query
        )