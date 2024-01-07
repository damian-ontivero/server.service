from dataclasses import dataclass

from st_server.shared.application.command import Command


@dataclass
class ModifyApplicationCommand(Command):
    id: str | None = None
    name: str | None = None
    version: str | None = None
    architect: str | None = None
