"""Represents the paginated query response."""

from dataclasses import dataclass, field

from st_server.shared.application.dto import DTO


@dataclass(frozen=True)
class QueryResponse:
    """Represents the paginated query response."""

    total: int
    limit: int
    offset: int
    items: list[DTO] = field(default_factory=list)

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
        """Return the query response as a dict."""
        return {
            "total": self.total,
            "limit": self.limit,
            "offset": self.offset,
            "prev_offset": self.prev_offset,
            "next_offset": self.next_offset,
            "items": [item.to_dict() for item in self.items],
        }
