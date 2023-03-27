"""Class to represent the response from the repository with pagination."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RepositoryResponse:
    """Class to represent the response from the repository with pagination."""

    total_items: int = None
    items: list = field(default_factory=list)
