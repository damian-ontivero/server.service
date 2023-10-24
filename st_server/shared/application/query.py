"""Base class for queries."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Query:
    """Base class for queries."""

    def to_dict(self) -> dict:
        return asdict(self)