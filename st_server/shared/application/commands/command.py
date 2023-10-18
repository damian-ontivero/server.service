"""Base class for commands."""

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Command:
    """Base class for commands."""

    def to_dict(self) -> dict:
        """Convert command to dict."""
        return asdict(self)
