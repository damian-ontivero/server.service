"""Base class for Data Transfer Objects."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DTO:
    """Base class for Data Transfer Objects."""

    def to_dict(self) -> dict:
        """Converts the DTO to a dictionary."""
        return asdict(self)
