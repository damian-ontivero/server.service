"""Class to represent the response from the Service with pagination."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServiceResponse:
    """Class to represent the response from the Service with pagination."""

    per_page: int = None
    page: int = None
    prev_page: int = None
    next_page: int = None
    last_page: int = None
    first_page: int = None
    items: list = field(default_factory=list)
