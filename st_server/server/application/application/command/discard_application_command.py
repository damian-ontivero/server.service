from dataclasses import dataclass

from st_server.shared.domain.bus.command.command import Command


@dataclass(frozen=True)
class DiscardApplicationCommand(Command):
    id: int
