import pytest

from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_application_query_handler import (
    FindManyApplicationQueryHandler,
)
from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.server.domain.application.application import Application
from st_server.shared.application.exception import NotFound
from tests.util.application.factory.application_factory import (
    ApplicationFactory,
)


def test_find_many_ok(mock_application_repository):
    applications = ApplicationFactory.create_batch(5)

    query = FindManyApplicationQuery(
        filter={
            "id": {
                "in": ",".join(
                    [application.id.value for application in applications]
                )
            }
        }
    )
    applications_found = FindManyApplicationQueryHandler(
        mock_application_repository
    ).handle(query)

    assert applications_found.total == 5
    assert isinstance(applications_found.items[0], Application)


def test_find_one_ok(mock_application_repository):
    application = ApplicationFactory()

    query = FindOneApplicationQuery(application.id.value)
    application_found = FindOneApplicationQueryHandler(
        mock_application_repository
    ).handle(query)

    assert isinstance(application_found, Application)
    assert application.id.value == application_found.id.value


def test_find_one_not_found(mock_application_repository):
    with pytest.raises(NotFound):
        query = FindOneApplicationQuery("1234")
        FindOneApplicationQueryHandler(mock_application_repository).handle(
            query
        )
