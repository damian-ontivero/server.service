"""Abstract class for command handlers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.command.application.command import Command


class CommandHandler(metaclass=ABCMeta):
    """Abstract class for command handlers."""

    @abstractmethod
    def __call__(self, command: Command) -> None:
        """Handle a command."""
        raise NotImplementedError
