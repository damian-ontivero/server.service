"""Contains the command handler class."""

from st_core.application.command_handler import CommandHandler
from st_core.application.exception import AlreadyExists
from st_core.infrastructure.message_bus import MessageBus

from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.dto.server import ServerDto
from st_server.server.domain.server.server_factory import ServerFactory
from st_server.server.domain.server.server_repository import ServerRepository


class AddServerCommandHandler(CommandHandler):
    """Command handler for adding a Server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddServerCommand) -> ServerDto:
        """Handle a command."""
        self._check_if_exists(command.name)
        server = ServerFactory.build(**command.to_dict())
        self._repository.save_one(server)
        for domain_event in server.domain_events:
            self._message_bus.publish(domain_event)
        server.clear_domain_events()
        return ServerDto.from_entity(server)

    def _check_if_exists(self, name: str) -> None:
        """Check if a Server with the given name already exists."""
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
