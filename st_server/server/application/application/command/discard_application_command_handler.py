from st_server.server.application.application.command.discard_application_command import (
    DiscardApplicationCommand,
)
from st_server.server.application.domain.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.exception import NotFound
from st_server.shared.domain.bus.command.command_handler import CommandHandler
from st_server.shared.domain.bus.event.event_bus import EventBus


class DiscardApplicationCommandHandler(CommandHandler):
    def __init__(
        self, repository: ApplicationRepository, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: DiscardApplicationCommand) -> None:
        application = self._repository.find_by_id(command.id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=command.id)
            )
        self._repository.delete_by_id(command.id)

        with self._event_bus:
            for domain_event in application.domain_events:
                self._event_bus.publish(domain_event)
        application.clear_domain_events()
