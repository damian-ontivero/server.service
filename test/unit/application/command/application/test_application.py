from st_server.server.application.dto.application import ApplicationReadDto
from test.util.factory.application_factory import ApplicationFactory
from st_server.server.application.command.application.add.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.command.application.update.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.command.application.delete.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.command.application.add.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from st_server.server.application.command.application.update.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
from st_server.server.application.command.application.delete.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)


def test_add_one_ok(mock_application_repository, mock_message_bus):
    application = ApplicationFactory.build()
    data = application.to_dict()

    command = AddApplicationCommand(
        name=data["name"],
        version=data["version"],
        architect=data["architect"],
    )
    AddApplicationCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_update_one_ok(mock_application_repository, mock_message_bus):
    application = ApplicationFactory()
    application.name = "SuperTest"

    command = UpdateApplicationCommand(
        id=application.id.value,
        name=application.name,
        version=application.version,
        architect=application.architect,
    )
    UpdateApplicationCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)


def test_delete_one_ok(mock_application_repository, mock_message_bus):
    application = ApplicationFactory()

    command = DeleteApplicationCommand(id=application.id.value)
    DeleteApplicationCommandHandler(
        repository=mock_application_repository, message_bus=mock_message_bus
    ).handle(command)
