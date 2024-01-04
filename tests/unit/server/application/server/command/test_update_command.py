from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.command.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from tests.util.server.domain.server.server_factory import ServerFactory


def test_update_one_ok(mock_server_repository, mock_rabbitmq_message_bus):
    server = ServerFactory()
    server.name = "SuperTest"

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment.value,
        operating_system=server.operating_system.__dict__,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status.value,
    )
    UpdateServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)


def test_update_one_blank_cpu_field_ok(
    mock_server_repository, mock_rabbitmq_message_bus
):
    server = ServerFactory()
    server.cpu = None

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment.value,
        operating_system=server.operating_system.__dict__,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status.value,
    )
    UpdateServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)


def test_update_one_blank_ram_field_ok(
    mock_server_repository, mock_rabbitmq_message_bus
):
    server = ServerFactory()
    server.ram = None

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment.value,
        operating_system=server.operating_system.__dict__,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status.value,
    )
    UpdateServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)


def test_update_one_blank_hdd_field_ok(
    mock_server_repository, mock_rabbitmq_message_bus
):
    server = ServerFactory()
    server.hdd = None

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment.value,
        operating_system=server.operating_system.__dict__,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status.value,
    )
    UpdateServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
