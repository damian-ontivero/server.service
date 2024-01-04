from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Query:
    """Base class for queries."""

    def to_dict(self) -> dict[str, any]:
        """Returns the dictionary representation of the query."""
        return asdict(self)
