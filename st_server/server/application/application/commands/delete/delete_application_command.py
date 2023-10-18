"""Commands for the Application."""

from dataclasses import dataclass

from st_server.shared.application.commands.command import Command


@dataclass(frozen=True)
class DeleteApplicationCommand(Command):
    """Command to delete an Application."""

    id: int
