from st_server.server.application.application.command.discard_application_command import (
    DiscardApplicationCommand,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.bus.message_bus import MessageBus
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import NotFound


class DiscardApplicationCommandHandler(CommandHandler):
    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: DiscardApplicationCommand) -> None:
        application = self._repository.find_by_id(command.id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=command.id)
            )
        self._repository.delete_by_id(command.id)
        for domain_event in application.domain_events:
            self._message_bus.publish(domain_event)
        application.clear_domain_events()
