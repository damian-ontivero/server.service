from dataclasses import dataclass

from st_server.shared.application.query import Query


@dataclass(frozen=True)
class FindOneServerQuery(Query):
    """Query to find one Server."""

    id: str
