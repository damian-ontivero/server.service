import pytest

from st_server.server.application.dtos.credential import CredentialReadDto
from st_server.shared.application.exceptions import NotFound
from tests.utils.factories.credential_factory import CredentialFactory


def test_find_many_ok(mock_credential_service):
    credentials = CredentialFactory.create_batch(5)

    credentials_found = mock_credential_service.find_many(
        id="in:{}".format(
            ",".join([credential.id.value for credential in credentials])
        )
    )

    assert credentials_found._total == 5
    assert isinstance(credentials_found._items[0], CredentialReadDto)


def test_find_one_ok(mock_credential_service):
    credential = CredentialFactory()

    credential_found = mock_credential_service.find_one(id=credential.id.value)

    assert isinstance(credential_found, CredentialReadDto)
    assert credential.id.value == credential_found.id


def test_find_one_not_found(mock_credential_service):
    with pytest.raises(NotFound):
        mock_credential_service.find_one(id="1234")


def test_add_one_ok(mock_credential_service):
    credential = CredentialFactory.build()
    data = credential.to_dict()

    credential_created = mock_credential_service.add_one(data=data)

    assert isinstance(credential_created, CredentialReadDto)
    assert credential.username == credential_created.username


def test_update_one_ok(mock_credential_service):
    credential = CredentialFactory()
    data = {"username": "SuperTest"}

    credential_updated = mock_credential_service.update_one(
        id=credential.id.value, data=data
    )

    assert isinstance(credential_updated, CredentialReadDto)
    assert credential_updated.username == data["username"]


def test_delete_one_ok(mock_credential_service):
    credential = CredentialFactory()

    mock_credential_service.delete_one(id=credential.id.value)
