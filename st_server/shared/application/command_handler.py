"""Abstract base class for command handlers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.application.command import Command


class CommandHandler(metaclass=ABCMeta):
    """Abstract base class for command handlers."""

    @abstractmethod
    def handle(self, command: Command) -> None:
        """Handle the command."""
        raise NotImplementedError
