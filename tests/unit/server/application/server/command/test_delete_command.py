"""Test for delete server command."""

from st_server.server.application.server.command.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.server.command.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from tests.util.server.domain.server.server_factory import ServerFactory


def test_delete_one_ok(mock_server_repository, mock_rabbitmq_message_bus):
    server = ServerFactory()

    command = DeleteServerCommand(server.id.value)
    DeleteServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
