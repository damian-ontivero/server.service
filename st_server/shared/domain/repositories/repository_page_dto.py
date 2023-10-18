from dataclasses import dataclass, field

from st_server.shared.domain.entities.entity import Entity


@dataclass(frozen=True)
class RepositoryPageDto:
    """Dataclass to represent the response from the repository with pagination."""

    total: int
    items: list[Entity] = field(default_factory=list)
