from dataclasses import dataclass, field

from st_server.shared.domain.aggregate_root import AggregateRoot


@dataclass(frozen=True)
class RepositoryResponse:
    """Dataclass to represent the response from the repository with pagination."""

    total: int
    items: list[AggregateRoot] = field(default_factory=list)
