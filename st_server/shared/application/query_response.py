"""Represents the paginated query response."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QueryResponse:
    """Represents the paginated query response."""

    total: int
    limit: int
    offset: int
    items: list = field(default_factory=list)

    @property
    def prev_offset(self) -> int | None:
        """Return the previous offset."""
        return self.offset - self.limit if self.offset > 0 else None

    @property
    def next_offset(self) -> int | None:
        """Return the next offset."""
        return (
            self.offset + self.limit
            if self.offset + self.limit < self.total
            else None
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the query response."""
        return {
            "total": self.total,
            "limit": self.limit,
            "offset": self.offset,
            "prev_offset": self.prev_offset,
            "next_offset": self.next_offset,
            "items": [item.to_dict() for item in self.items],
        }
