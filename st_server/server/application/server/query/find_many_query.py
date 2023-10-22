"""Query to find many Servers."""

from dataclasses import dataclass

from st_server.shared.application.query import Query


@dataclass(frozen=True)
class FindManyServerQuery(Query):
    """Query to find many Servers."""

    limit: int | None = None
    offset: int | None = None
    filter: dict | None = None
    and_filter: list[dict] | None = None
    or_filter: list[dict] | None = None
    sort: list[dict] | None = None
