from dataclasses import dataclass, field
from typing import List

from st_server.shared.domain.aggregate_root import AggregateRoot


@dataclass(frozen=True)
class RepositoryResponse:
    """Represents the response from the repository with pagination."""

    total: int
    items: List[AggregateRoot] = field(default_factory=list)
