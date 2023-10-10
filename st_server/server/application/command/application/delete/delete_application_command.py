"""Commands for the application."""

from dataclasses import dataclass

from st_server.shared.application.command.command import Command


@dataclass(frozen=True)
class DeleteApplicationCommand(Command):
    """Command to delete an application."""

    id: int
