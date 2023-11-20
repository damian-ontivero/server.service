"""Query to find many Servers."""

from dataclasses import dataclass, field

from st_core.application.query import Query


@dataclass(frozen=True)
class FindManyServerQuery(Query):
    """Query to find many Servers."""

    limit: int | None = None
    offset: int | None = None
    filter: dict | None = None
    and_filter: list[dict] = field(default_factory=list)
    or_filter: list[dict] = field(default_factory=list)
    sort: list[dict] = field(default_factory=list)
