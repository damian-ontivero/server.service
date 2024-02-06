from st_server.server.server.application.command.register_server_command import (
    RegisterServerCommand,
)
from st_server.server.server.application.command.register_server_command_handler import (
    RegisterServerCommandHandler,
)
from tests.util.server.domain.server.server_factory import ServerFactory


def test_register_ok(mock_server_repository, mock_rabbitmq_message_bus):
    server = ServerFactory.build()

    command = RegisterServerCommand(
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment.value,
        operating_system=server.operating_system.__dict__,
        credentials=server.credentials,
        applications=server.applications,
    )
    RegisterServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
