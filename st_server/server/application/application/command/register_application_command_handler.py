from st_server.server.application.application.command.register_application_command import (
    RegisterApplicationCommand,
)
from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.domain.application import Application
from st_server.server.application.domain.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.exception import AlreadyExists
from st_server.shared.domain.bus.command.command_handler import CommandHandler
from st_server.shared.domain.bus.event.event_bus import EventBus


class RegisterApplicationCommandHandler(CommandHandler):
    def __init__(
        self, repository: ApplicationRepository, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: RegisterApplicationCommand) -> ApplicationDto:
        application = Application.register(
            name=command.name,
            version=command.version,
            architect=command.architect,
        )
        self._check_if_exists(application.name)
        self._repository.add(application)

        with self._event_bus:
            for domain_event in application.domain_events:
                self._event_bus.publish(domain_event)
        application.clear_domain_events()

        return ApplicationDto.from_entity(application)

    def _check_if_exists(self, name: str) -> None:
        applications = self._repository.find_many(
            filter={"name": {"eq": name}}
        )
        if applications.total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
