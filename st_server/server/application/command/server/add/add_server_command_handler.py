"""Contains the command handler class."""

from st_server.shared.application.command.commad_handler import CommandHandler
from st_server.shared.application.exception.exception import AlreadyExists
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus
from st_server.server.application.command.server.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.dto.server import ServerReadDto
from st_server.server.domain.entity.server import Server
from st_server.server.domain.repository.server_repository import (
    ServerRepository,
)


class AddServerCommandHandler(CommandHandler):
    """Command handler for adding a server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddServerCommand) -> int:
        """Handle a command."""
        server = Server.create(name=command.name)
        self._check_exists(name=server.name)
        self._repository.save_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
        server = self._repository.find_one(id=server.id.value)
        return ServerReadDto.from_entity(server=server)

    def _check_exists(self, name: str) -> None:
        """Returns True if a server with the given name exists."""
        servers = self._repository.find_many(_filter={"name": {"eq": name}})
        if servers._total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
