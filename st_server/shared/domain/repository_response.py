from dataclasses import dataclass, field

from st_server.shared.domain.aggregate_root import AggregateRoot


@dataclass(frozen=True)
class RepositoryResponse:
    total: int
    items: list[AggregateRoot] = field(default_factory=list)
