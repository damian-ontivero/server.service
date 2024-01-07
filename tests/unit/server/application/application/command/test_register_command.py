from st_server.server.application.application.command.register_application_command import (
    RegisterApplicationCommand,
)
from st_server.server.application.application.command.register_application_command_handler import (
    RegisterApplicationCommandHandler,
)
from tests.util.server.domain.application.application_factory import (
    ApplicationFactory,
)


def test_register_ok(mock_application_repository, mock_rabbitmq_message_bus):
    application = ApplicationFactory.build()

    command = RegisterApplicationCommand(
        name=application.name,
        version=application.version,
        architect=application.architect,
    )
    RegisterApplicationCommandHandler(
        repository=mock_application_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
