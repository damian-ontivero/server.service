"""Dataclasses to represent response objects."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RepositoryResponse:
    """Dataclass to represent the response from the repository with pagination."""

    total_items: int | None = None
    items: list = field(default_factory=list)


@dataclass(frozen=True)
class ServiceResponse:
    """Dataclass to represent the response from the Service with pagination."""

    limit: int | None = None
    offset: int | None = None
    prev_offset: int | None = None
    next_offset: int | None = None
    last_offset: int | None = None
    first_offset: int | None = None
    items: list = field(default_factory=list)
