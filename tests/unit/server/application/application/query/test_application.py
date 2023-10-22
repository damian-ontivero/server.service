import pytest

from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.shared.application.exception import NotFound
from tests.util.factory.application_factory import ApplicationFactory


def test_find_many_ok(mock_application_query):
    applications = ApplicationFactory.create_batch(5)

    applications_found = mock_application_query.find_many(
        filter={
            "id": {
                "in": ",".join(
                    [application.id.value for application in applications]
                )
            }
        }
    )

    assert applications_found.total == 5
    assert isinstance(applications_found.items[0], ApplicationReadDto)


def test_find_one_ok(mock_application_query):
    application = ApplicationFactory()

    application_found = mock_application_query.find_one(application.id.value)

    assert isinstance(application_found, ApplicationReadDto)
    assert application.id.value == application_found.id


def test_find_one_not_found(mock_application_query):
    with pytest.raises(NotFound):
        mock_application_query.find_one("1234")