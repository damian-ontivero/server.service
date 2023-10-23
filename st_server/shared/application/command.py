"""Base class for commands."""

from dataclasses import asdict, dataclass


@dataclass
class Command:
    """Base class for commands."""

    def to_dict(self) -> dict:
        return asdict(self)
