from st_server.server.application.server.command.register_server_command import (
    RegisterServerCommand,
)
from st_server.server.application.server.dto.server import ServerDto
from st_server.server.domain.server.environment import Environment
from st_server.server.domain.server.operating_system import OperatingSystem
from st_server.server.domain.server.server import Server
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.server.domain.server.server_status import ServerStatus
from st_server.shared.application.bus.message_bus import MessageBus
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import AlreadyExists


class RegisterServerCommandHandler(CommandHandler):
    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: RegisterServerCommand) -> ServerDto:
        self._check_if_exists(command.name)
        server = Server.register(**command.to_dict())
        self._repository.add(server)
        for domain_event in server.domain_events:
            self._message_bus.publish(domain_event)
        server.clear_domain_events()
        return ServerDto.from_entity(server)

    def _check_if_exists(self, name: str) -> None:
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )