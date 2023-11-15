"""Base class for data transfer objects."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DTO:
    """Base class for data transfer objects."""

    def to_dict(self) -> dict:
        """Converts the data transfer object to a dictionary."""
        return asdict(self)
