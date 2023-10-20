from st_server.server.application.command.application.add.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.command.application.add.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from st_server.server.application.command.application.delete.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.command.application.delete.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)
from st_server.server.application.command.application.update.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.command.application.update.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
from tests.util.factories.application_factory import ApplicationFactory


def test_add_one_ok(mock_application_repository, mock_message_bus):
    application = ApplicationFactory.build()

    command = AddApplicationCommand(
        name=application.name,
        version=application.version,
        architect=application.architect,
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
