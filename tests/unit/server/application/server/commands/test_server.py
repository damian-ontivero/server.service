from st_server.server.application.server.commands.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.commands.add.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.server.commands.delete.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.server.commands.delete.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from st_server.server.application.server.commands.update.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.commands.update.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from tests.util.factories.server_factory import ServerFactory


def test_add_one_ok(mock_server_repository, mock_message_bus):
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
        repository=mock_server_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_ok(mock_server_repository, mock_message_bus):
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
        repository=mock_server_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_blank_cpu_field_ok(
    mock_server_repository, mock_message_bus
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
        repository=mock_server_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_blank_ram_field_ok(
    mock_server_repository, mock_message_bus
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
        repository=mock_server_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_blank_hdd_field_ok(
    mock_server_repository, mock_message_bus
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
        repository=mock_server_repository, message_bus=mock_message_bus
    ).handle(command)


def test_delete_one_ok(mock_server_repository, mock_message_bus):
    server = ServerFactory()

    command = DeleteServerCommand(server.id.value)
    DeleteServerCommandHandler(
        repository=mock_server_repository, message_bus=mock_message_bus
    ).handle(command)
