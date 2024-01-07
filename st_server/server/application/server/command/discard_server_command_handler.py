from st_server.server.application.server.command.discard_server_command import (
    DiscardServerCommand,
)
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.bus.message_bus import MessageBus
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import NotFound


class DiscardServerCommandHandler(CommandHandler):
    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: DiscardServerCommand) -> None:
        server = self._repository.find_by_id(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        server.discard()
        self._repository.update(command.id)
        for domain_event in server.domain_events:
            self._message_bus.publish(domain_event)
        server.clear_domain_events()
