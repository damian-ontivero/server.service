"""Config file for pytest."""

import pytest


@pytest.fixture(scope="function", autouse=True)
def mock_message_bus():
    from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
        RabbitMQMessageBus,
    )

    message_bus = RabbitMQMessageBus(
        host="localhost", port=5672, username="admin", password="admin"
    )
    # message_bus = RabbitMQMessageBus(
    #     host="192.168.1.63", port=5672, username="admin", password="st4dM1n!"
    # )
    yield message_bus


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
    from st_server.server.infrastructure.mysql.repository.server_repository import (
        ServerRepositoryImpl,
    )

    yield ServerRepositoryImpl(session=mock_session)


@pytest.fixture(scope="function")
def mock_server_query(mock_server_repository, mock_message_bus):
    from st_server.server.application.query.server.server_query import (
        ServerQuery,
    )

    yield ServerQuery(
        repository=mock_server_repository,
        message_bus=mock_message_bus,
    )


@pytest.fixture(scope="function")
def mock_application_repository(mock_session, test_db):
    from st_server.server.infrastructure.mysql.repository.application_repository import (
        ApplicationRepositoryImpl,
    )

    yield ApplicationRepositoryImpl(session=mock_session)


@pytest.fixture(scope="function")
def mock_application_query(mock_application_repository, mock_message_bus):
    from st_server.server.application.query.application.application_query import (
        ApplicationQuery,
    )

    yield ApplicationQuery(
        repository=mock_application_repository,
        message_bus=mock_message_bus,
    )


# @pytest.fixture(scope="function")
# def mock_auth_service(mock_user_repository):
#     from st_server.server.application.services.auth import AuthService

#     auth_service = AuthService(repository=mock_user_repository)
#     yield auth_service
