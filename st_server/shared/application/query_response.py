from dataclasses import dataclass, field
from typing import List, Union


@dataclass(frozen=True)
class QueryResponse:
    """Represents the paginated query response."""

    total: int
    limit: int
    offset: int
    items: List = field(default_factory=list)

    @property
    def prev_offset(self) -> Union[int, None]:
        """Returns the previous offset if available."""
        return self.offset - self.limit if self.offset > 0 else None

    @property
    def next_offset(self) -> Union[int, None]:
        """Returns the next offset if available."""
        return (
            self.offset + self.limit
            if self.offset + self.limit < self.total
            else None
        )

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the query response."""
        return {
            "total": self.total,
            "limit": self.limit,
            "offset": self.offset,
            "prev_offset": self.prev_offset,
            "next_offset": self.next_offset,
            "items": [item.to_dict() for item in self.items],
        }
