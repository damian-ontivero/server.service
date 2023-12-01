"""Test for find many application query."""

from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_application_query_handler import (
    FindManyApplicationQueryHandler,
)
from tests.util.server.domain.application.application_factory import (
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
    assert isinstance(applications_found.items[0], ApplicationDto)
