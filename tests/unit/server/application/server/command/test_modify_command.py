from st_server.server.server.application.command.modify_server_command import (
    ModifyServerCommand,
)
from st_server.server.server.application.command.modify_server_command_handler import (
    ModifyServerCommandHandler,
)
from st_server.server.server.domain.server import Server
from tests.util.server.domain.server.server_factory import ServerFactory


def test_modify_name_ok(mock_server_repository, mock_rabbitmq_message_bus):
    # Build a server.
    server = ServerFactory()

    # Modify the name.
    server.name = "unit_test"

    # Build the command.
    command = ModifyServerCommand(
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

    # Execute the command.
    ModifyServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)

    # Check the server was updated.
    saved_server = mock_server_repository.find_by_id(server.id.value)
    assert saved_server is not None
    assert saved_server.id == server.id
    assert saved_server.name == "unit_test"


def test_modify_domain_event_registered(
    mock_server_repository, mock_rabbitmq_message_bus
):
    # Build a server.
    server = ServerFactory()

    # Modify the status.
    server.status = "modified"

    # Build the command.
    command = ModifyServerCommand(
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

    # Execute the command.
    ModifyServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)

    # Check the event was published.
    assert server.domain_events is not None
    assert len(server.domain_events) == 1
    assert isinstance(server.domain_events[0], Server.Modified)


def test_modify_cpu_with_none(
    mock_server_repository, mock_rabbitmq_message_bus
):
    server = ServerFactory()
    server.cpu = None

    command = ModifyServerCommand(
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
    ModifyServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)


def test_modify_ram_with_none(
    mock_server_repository, mock_rabbitmq_message_bus
):
    server = ServerFactory()
    server.ram = None

    command = ModifyServerCommand(
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
    ModifyServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)


def test_modify_hdd_with_none(
    mock_server_repository, mock_rabbitmq_message_bus
):
    server = ServerFactory()
    server.hdd = None

    command = ModifyServerCommand(
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
    ModifyServerCommandHandler(
        repository=mock_server_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
