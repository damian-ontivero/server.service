"""Dataclasses to represent the paginated query response."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QueryResponse:
    """Dataclass to represent the paginated query response."""

    _total: int
    _limit: int
    _offset: int
    _prev_offset: int | None = None
    _next_offset: int | None = None
    _items: list = field(default_factory=list)
