"""Test for delete application command."""

from st_server.server.application.application.command.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.application.command.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)
from tests.util.server.domain.application.application_factory import (
    ApplicationFactory,
)


def test_delete_one_ok(mock_application_repository, mock_rabbitmq_message_bus):
    application = ApplicationFactory()

    command = DeleteApplicationCommand(id=application.id.value)
    DeleteApplicationCommandHandler(
        repository=mock_application_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
