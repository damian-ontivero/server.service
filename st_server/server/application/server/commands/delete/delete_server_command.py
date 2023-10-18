"""Commands for the Server."""

from dataclasses import dataclass

from st_server.shared.application.commands.command import Command


@dataclass(frozen=True)
class DeleteServerCommand(Command):
    """Command to delete a Server."""

    id: int
