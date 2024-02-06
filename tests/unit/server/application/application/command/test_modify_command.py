from st_server.server.application.application.command.modify_application_command import (
    ModifyApplicationCommand,
)
from st_server.server.application.application.command.modify_application_command_handler import (
    ModifyApplicationCommandHandler,
)
from tests.util.server.domain.application.application_factory import ApplicationFactory


def test_modify_one_ok(mock_application_repository, mock_rabbitmq_message_bus):
    application = ApplicationFactory()
    application.name = "SuperTest"

    command = ModifyApplicationCommand(
        id=application.id.value,
        name=application.name,
        version=application.version,
        architect=application.architect,
    )
    ModifyApplicationCommandHandler(
        repository=mock_application_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
