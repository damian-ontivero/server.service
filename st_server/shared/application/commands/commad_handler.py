"""Abstract class for command handlers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.application.commands.command import Command


class CommandHandler(metaclass=ABCMeta):
    """Abstract class for command handlers."""

    @abstractmethod
    def handle(self, command: Command) -> None:
        """Handle a command."""
        raise NotImplementedError
