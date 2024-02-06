from st_server.server.server.application.command.register_server_command import (
    RegisterServerCommand,
)
from st_server.server.server.application.dto.server import ServerDto
from st_server.server.server.domain.server import Server
from st_server.server.server.domain.server_repository import ServerRepository
from st_server.shared.application.exception import AlreadyExists
from st_server.shared.domain.bus.command.command_handler import CommandHandler
from st_server.shared.domain.bus.event.event_bus import EventBus


class RegisterServerCommandHandler(CommandHandler):
    def __init__(
        self, repository: ServerRepository, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: RegisterServerCommand) -> ServerDto:
        self._check_if_exists(command.name)
        server = Server.register(
            name=command.name,
            cpu=command.cpu,
            ram=command.ram,
            hdd=command.hdd,
            environment=command.environment,
            operating_system=command.operating_system,
            credentials=command.credentials,
            applications=command.applications,
        )
        self._repository.add(server)

        with self._event_bus:
            for domain_event in server.domain_events:
                self._event_bus.publish(domain_event)
        server.clear_domain_events()

        return ServerDto.from_entity(server)

    def _check_if_exists(self, name: str) -> None:
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
