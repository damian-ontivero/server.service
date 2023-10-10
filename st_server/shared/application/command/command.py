"""Base class for commands."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    """Base class for commands."""
