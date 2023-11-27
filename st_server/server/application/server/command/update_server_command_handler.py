"""Contains the command handler class."""

from st_core.application.command_handler import CommandHandler
from st_core.application.exception import AlreadyExists, NotFound
from st_core.application.message_bus import MessageBus

from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.dto.server import ServerDto
from st_server.server.domain.server.server_repository import ServerRepository


class UpdateServerCommandHandler(CommandHandler):
    """Command handler for updating a Server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: UpdateServerCommand) -> ServerDto:
        """Handle a command."""
        server = self._repository.find_one(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        if not server.name == command.name:
            self._check_if_exists(command.name)
        server.update(
            name=command.name,
            cpu=command.cpu,
            ram=command.ram,
            hdd=command.hdd,
            environment=command.environment,
            operating_system=command.operating_system,
            credentials=command.credentials,
            applications=command.applications,
            status=command.status,
        )
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
