"""Abstract class for command handlers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.application.command.command import Command


class CommandHandler(metaclass=ABCMeta):
    """Abstract class for command handlers."""

    @abstractmethod
    def __call__(self, command: Command) -> None:
        raise NotImplementedError
