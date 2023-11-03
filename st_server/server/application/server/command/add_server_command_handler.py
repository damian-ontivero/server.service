"""Contains the command handler class."""

from st_server.server.application.command_bus.message_bus import MessageBus
from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.domain.server.server import Server
from st_server.server.domain.server.server_factory import ServerFactory
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import AlreadyExists


class AddServerCommandHandler(CommandHandler):
    """Command handler for adding a Server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddServerCommand) -> Server:
        """Handle a command."""
        self._check_if_exists(command.name)
        server = ServerFactory.build(**command.to_dict())
        self._repository.save_one(server)
        self._message_bus.publish(server.domain_events)
        server.clear_domain_events()
        return server

    def _check_if_exists(self, name: str) -> None:
        """Check if a Server with the given name already exists."""
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
