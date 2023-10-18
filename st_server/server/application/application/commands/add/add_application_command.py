"""Commands for the Application."""

from dataclasses import dataclass

from st_server.shared.application.commands.command import Command


@dataclass(frozen=True)
class AddApplicationCommand(Command):
    """Command to add a Application."""

    name: str
    version: str
    architect: str