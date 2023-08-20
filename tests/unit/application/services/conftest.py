"""Config file for pytest."""

import pytest


@pytest.fixture(scope="function", autouse=True)
def mock_message_bus():
    from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
        RabbitMQMessageBus,
    )

    yield RabbitMQMessageBus(
        host="localhost", port=5672, username="admin", password="admin"
    )


# @pytest.fixture(scope="function", autouse=True)
# def mock_decorator(monkeypatch: pytest.MonkeyPatch):
#     from functools import wraps

#     from st_server.server.application.services import auth
#     from st_server.server.infrastructure.acl import acl

#     def fake_decorator(func):
#         @wraps(func)
#         def wrapped(*args, **kwargs):
#             return func(*args, **kwargs)

#         return wrapped

#     monkeypatch.setattr(auth, "validate_access_token", fake_decorator)
#     monkeypatch.setattr(acl, "validate_permission", fake_decorator)


@pytest.fixture(scope="function")
def mock_server_repository(mock_session, test_db):
    from st_server.server.infrastructure.mysql.repositories.server_repository import (
        ServerRepositoryImpl,
    )

    yield ServerRepositoryImpl(session=mock_session)


@pytest.fixture(scope="function")
def mock_server_service(mock_server_repository, mock_message_bus):
    from st_server.server.application.services.server import ServerService

    yield ServerService(
        repository=mock_server_repository,
        message_bus=mock_message_bus,
    )


@pytest.fixture(scope="function")
def mock_application_repository(mock_session, test_db):
    from st_server.server.infrastructure.mysql.repositories.application_repository import (
        ApplicationRepositoryImpl,
    )

    yield ApplicationRepositoryImpl(session=mock_session)


@pytest.fixture(scope="function")
def mock_application_service(mock_application_repository, mock_message_bus):
    from st_server.server.application.services.application import (
        ApplicationService,
    )

    yield ApplicationService(
        repository=mock_application_repository,
        message_bus=mock_message_bus,
    )


# @pytest.fixture(scope="function")
# def mock_auth_service(mock_user_repository):
#     from st_server.server.application.services.auth import AuthService

#     auth_service = AuthService(repository=mock_user_repository)
#     yield auth_service
