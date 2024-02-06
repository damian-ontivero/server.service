from dataclasses import dataclass, field

from st_server.shared.domain.bus.query.query import Query


@dataclass(frozen=True)
class FindManyApplicationQuery(Query):
    limit: int | None = None
    offset: int | None = None
    filter: dict | None = None
    and_filter: list[dict] = field(default_factory=list)
    or_filter: list[dict] = field(default_factory=list)
    sort: list[dict] = field(default_factory=list)
