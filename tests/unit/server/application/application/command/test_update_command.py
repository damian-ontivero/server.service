from st_server.server.application.application.command.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.application.command.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
from tests.util.server.domain.application.application_factory import (
    ApplicationFactory,
)


def test_update_one_ok(mock_application_repository, mock_rabbitmq_message_bus):
    application = ApplicationFactory()
    application.name = "SuperTest"

    command = UpdateApplicationCommand(
        id=application.id.value,
        name=application.name,
        version=application.version,
        architect=application.architect,
    )
    UpdateApplicationCommandHandler(
        repository=mock_application_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
