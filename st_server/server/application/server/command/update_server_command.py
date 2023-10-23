"""Commands for the Server."""

from dataclasses import dataclass, field

from st_server.shared.application.command import Command


@dataclass(frozen=True)
class UpdateServerCommand(Command):
    """Command to update a Server."""

    id: str
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: dict | None = None
    operating_system: dict | None = None
    credentials: list[dict] = field(default_factory=list)
    applications: list[dict] = field(default_factory=list)
    status: str | None = None
