"""Base class for command bus."""

from st_server.shared.application.command import Command
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.domain.repository import Repository
from st_server.shared.infrastructure.message_bus import MessageBus


class BaseCommandBus:
    """Base class for command bus.

    Command bus is a mechanism for dispatching commands.
    """

    def __init__(self, repository: Repository, message_bus: MessageBus):
        """Initialize the command bus."""
        self._repository = repository
        self._message_bus = message_bus
        self._handlers: dict[type[Command], CommandHandler] = dict()

    def dispatch(self, command: Command) -> None:
        """Dispatch a command."""
        handler = self._handlers.get(type(command))
        if handler is None:
            raise Exception("No handler registered for command")
        handler = handler(
            repository=self._repository, message_bus=self._message_bus
        )
        handler(command)
