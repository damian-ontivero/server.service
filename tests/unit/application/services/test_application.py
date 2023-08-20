import pytest

from st_server.server.application.dtos.application import ApplicationReadDto
from st_server.shared.application.exceptions import NotFound
from tests.utils.factories.application_factory import ApplicationFactory


def test_find_many_ok(mock_application_service):
    applications = ApplicationFactory.create_batch(5)

    applications_found = mock_application_service.find_many(
        id="in:{}".format(
            ",".join([application.id.value for application in applications])
        )
    )

    assert applications_found._total == 5
    assert isinstance(applications_found._items[0], ApplicationReadDto)


def test_find_one_ok(mock_application_service):
    application = ApplicationFactory()

    application_found = mock_application_service.find_one(
        id=application.id.value
    )

    assert isinstance(application_found, ApplicationReadDto)
    assert application.id.value == application_found.id


def test_find_one_not_found(mock_application_service):
    with pytest.raises(NotFound):
        mock_application_service.find_one(id="1234")


def test_add_one_ok(mock_application_service):
    application = ApplicationFactory.build()
    data = application.to_dict()

    application_created = mock_application_service.add_one(data=data)

    assert isinstance(application_created, ApplicationReadDto)
    assert application.name == application_created.name


def test_update_one_ok(mock_application_service):
    application = ApplicationFactory()
    data = {"name": "SuperTest"}

    application_updated = mock_application_service.update_one(
        id=application.id.value, data=data
    )

    assert isinstance(application_updated, ApplicationReadDto)
    assert application_updated.name == data["name"]


def test_delete_one_ok(mock_application_service):
    application = ApplicationFactory()

    mock_application_service.delete_one(id=application.id.value)
