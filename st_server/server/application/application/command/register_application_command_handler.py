from st_server.server.application.application.command.register_application_command import (
    RegisterApplicationCommand,
)
from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.domain.application.application import Application
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.bus.message_bus import MessageBus
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import AlreadyExists


class RegisterApplicationCommandHandler(CommandHandler):
    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: RegisterApplicationCommand) -> ApplicationDto:
        application = Application.register(**command.to_dict())
        self._check_if_exists(application.name)
        self._repository.add(application)
        for domain_event in application.domain_events:
            self._message_bus.publish(domain_event)
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
