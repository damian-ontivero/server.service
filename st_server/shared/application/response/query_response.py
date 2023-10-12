"""Dataclasses to represent the paginated query response."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QueryResponse:
    """Dataclass to represent the paginated query response."""

    total: int
    limit: int
    offset: int
    prev_offset: int | None = None
    next_offset: int | None = None
    items: list = field(default_factory=list)
