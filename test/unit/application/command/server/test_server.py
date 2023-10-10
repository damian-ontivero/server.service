from st_server.server.application.dto.server import ServerReadDto
from test.util.factory.server_factory import ServerFactory
from st_server.server.application.command.server.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.command.server.update.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.command.server.delete.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.command.server.add.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.command.server.update.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.server.application.command.server.delete.delete_server_command_handler import (
    DeleteServerCommandHandler,
)


def test_add_one_ok(mock_application_repository, mock_message_bus):
    server = ServerFactory.build()
    data = server.to_dict()

    command = AddServerCommand(
        name=data["name"],
        cpu=data["cpu"],
        ram=data["ram"],
        hdd=data["hdd"],
        environment=data["environment"],
        operating_system=data["operating_system"],
        credentials=data["credentials"],
        applications=data["applications"],
    )
    AddServerCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_ok(mock_application_repository, mock_message_bus):
    server = ServerFactory()
    server.name = "SuperTest"

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment,
        operating_system=server.operating_system,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status,
    )
    UpdateServerCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_blank_cpu_field_ok(
    mock_application_repository, mock_message_bus
):
    server = ServerFactory()
    server.cpu = None

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment,
        operating_system=server.operating_system,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status,
    )
    UpdateServerCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_blank_ram_field_ok(
    mock_application_repository, mock_message_bus
):
    server = ServerFactory()
    server.ram = None

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment,
        operating_system=server.operating_system,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status,
    )
    UpdateServerCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_blank_hdd_field_ok(
    mock_application_repository, mock_message_bus
):
    server = ServerFactory()
    server.hdd = None

    command = UpdateServerCommand(
        id=server.id.value,
        name=server.name,
        cpu=server.cpu,
        ram=server.ram,
        hdd=server.hdd,
        environment=server.environment,
        operating_system=server.operating_system,
        credentials=server.credentials,
        applications=server.applications,
        status=server.status,
    )
    UpdateServerCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_delete_one_ok(mock_application_repository, mock_message_bus):
    server = ServerFactory()

    command = DeleteServerCommand(id=server.id.value)
    DeleteServerCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)
