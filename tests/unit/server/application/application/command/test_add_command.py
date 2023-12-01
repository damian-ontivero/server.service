"""Test for add application command."""

from st_server.server.application.application.command.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.command.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from tests.util.server.domain.application.application_factory import (
    ApplicationFactory,
)


def test_add_one_ok(mock_application_repository, mock_rabbitmq_message_bus):
    application = ApplicationFactory.build()

    command = AddApplicationCommand(
        name=application.name,
        version=application.version,
        architect=application.architect,
    )
    AddApplicationCommandHandler(
        repository=mock_application_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
