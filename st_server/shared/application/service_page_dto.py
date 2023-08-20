"""Dataclasses to represent the paginated service response."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServicePageDto:
    """Dataclass to represent the paginated service response."""

    _total: int
    _limit: int
    _offset: int
    _prev_offset: int | None = None
    _next_offset: int | None = None
    _items: list = field(default_factory=list)
