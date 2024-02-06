from st_server.server.server.application.command.discard_server_command import (
    DiscardServerCommand,
)
from st_server.server.server.domain.server_repository import ServerRepository
from st_server.shared.application.exception import NotFound
from st_server.shared.domain.bus.command.command_handler import CommandHandler
from st_server.shared.domain.bus.event.event_bus import EventBus


class DiscardServerCommandHandler(CommandHandler):
    def __init__(
        self, repository: ServerRepository, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: DiscardServerCommand) -> None:
        server = self._repository.find_by_id(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        server.discard()
        self._repository.update(command.id)

        with self._event_bus:
            for domain_event in server.domain_events:
                self._event_bus.publish(domain_event)
        server.clear_domain_events()
