"""Test for add server command."""

from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.command.add_server_command_handler import (
    AddServerCommandHandler,
)
from tests.util.server.domain.server.server_factory import ServerFactory


def test_add_one_ok(mock_server_repository, mock_rabbitmq_message_bus):
    server = ServerFactory.build()

    command = AddServerCommand(
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment.value,
        operating_system=server.operating_system.__dict__,
        credentials=server.credentials,
        applications=server.applications,
    )
    AddServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
