"""Commands for the application."""

from dataclasses import dataclass

from st_server.shared.application.command.command import Command


@dataclass(frozen=True)
class AddServerCommand(Command):
    """Command to add a server."""

    name: str
    cpu: str
    ram: str
    hdd: str
    environment: dict
    operating_system: dict
    credentials: list[dict]
    applications: list[dict]
