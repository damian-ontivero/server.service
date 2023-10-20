"""Base class for all controllers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.command.application.command import Command


class Controller(metaclass=ABCMeta):
    """Base class for all controllers."""

    @abstractmethod
    def __call__(self, command: Command):
        """Handle the given command."""
        pass
