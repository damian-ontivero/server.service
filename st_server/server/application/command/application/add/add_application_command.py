"""Commands for the application."""

from dataclasses import dataclass

from st_server.shared.application.command.command import Command


@dataclass(frozen=True)
class AddApplicationCommand(Command):
    """Command to add a application."""

    name: str
    version: str
    architect: str
