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

    per_page: int | None = None
    page: int | None = None
    prev_page: int | None = None
    next_page: int | None = None
    last_page: int | None = None
    first_page: int | None = None
    items: list = field(default_factory=list)
