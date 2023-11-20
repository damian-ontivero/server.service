"""Commands for the Application."""

from dataclasses import dataclass

from st_core.application.command import Command


@dataclass
class AddApplicationCommand(Command):
    """Command to add a Application."""

    name: str | None = None
    version: str | None = None
    architect: str | None = None
