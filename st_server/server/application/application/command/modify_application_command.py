from dataclasses import dataclass

from st_server.shared.domain.bus.command.command import Command


@dataclass(frozen=True)
class ModifyApplicationCommand(Command):
    id: str | None = None
    name: str | None = None
    version: str | None = None
    architect: str | None = None
