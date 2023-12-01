"""Config file for pytest."""

import pytest


@pytest.fixture(scope="function", autouse=True)
def mock_rabbitmq_message_bus():
    from tests.util.shared.infrastructure.message_bus.rabbitmq_fake import (
        RabbitMQFake,
    )

    yield RabbitMQFake()


@pytest.fixture(scope="function")
def mock_server_repository(mock_session, test_db):
    from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
        ServerRepositoryImpl,
    )

    yield ServerRepositoryImpl(mock_session)


@pytest.fixture(scope="function")
def mock_application_repository(mock_session, test_db):
    from st_server.server.infrastructure.persistence.mysql.application.application_repository import (
        ApplicationRepositoryImpl,
    )

    yield ApplicationRepositoryImpl(mock_session)
