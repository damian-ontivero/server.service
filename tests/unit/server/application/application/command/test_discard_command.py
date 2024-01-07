from st_server.server.application.application.command.discard_application_command import (
    DiscardApplicationCommand,
)
from st_server.server.application.application.command.discard_application_command_handler import (
    DiscardApplicationCommandHandler,
)
from tests.util.server.domain.application.application_factory import (
    ApplicationFactory,
)


def test_discard_one_ok(
    mock_application_repository, mock_rabbitmq_message_bus
):
    application = ApplicationFactory()

    command = DiscardApplicationCommand(id=application.id.value)
    DiscardApplicationCommandHandler(
        repository=mock_application_repository,
        message_bus=mock_rabbitmq_message_bus,
    ).handle(command)
