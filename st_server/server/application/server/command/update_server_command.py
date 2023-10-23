"""Commands for the Server."""

from dataclasses import dataclass, field

from st_server.shared.application.command import Command


@dataclass
class UpdateServerCommand(Command):
    """Command to update a Server."""

    id: str | None = None
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[dict] = field(default_factory=list)
    applications: list[dict] = field(default_factory=list)
    status: str | None = None
