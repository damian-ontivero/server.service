from dataclasses import asdict, dataclass
from typing import Dict


@dataclass(frozen=True)
class Query:
    """Base class for queries."""

    def to_dict(self) -> Dict[str, any]:
        """Returns the dictionary representation of the query."""
        return asdict(self)
