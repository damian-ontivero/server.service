import pytest

from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.server.application.application.query.find_many_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_query_handler import (
    FindManyApplicationQueryHandler,
)
from st_server.server.application.application.query.find_one_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.shared.application.exception import NotFound
from tests.util.factory.application_factory import ApplicationFactory


def test_find_many_ok():
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
    applications_found = FindManyApplicationQueryHandler().handle(query)

    assert applications_found.total == 5
    assert isinstance(applications_found.items[0], ApplicationReadDto)


def test_find_one_ok():
    application = ApplicationFactory()

    query = FindOneApplicationQuery(application.id.value)
    application_found = FindOneApplicationQueryHandler().handle(query)

    assert isinstance(application_found, ApplicationReadDto)
    assert application.id.value == application_found.id


def test_find_one_not_found():
    with pytest.raises(NotFound):
        query = FindOneApplicationQuery("1234")
        FindOneApplicationQueryHandler().handle(query)
