from st_server.server.application.server.command.discard_server_command import (
    DiscardServerCommand,
)
from st_server.server.application.server.command.discard_server_command_handler import (
    DiscardServerCommandHandler,
)
from tests.util.server.domain.server.server_factory import ServerFactory


def test_discard_one_ok(mock_server_repository, mock_rabbitmq_message_bus):
    server = ServerFactory()

    command = DiscardServerCommand(server.id.value)
    DiscardServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
