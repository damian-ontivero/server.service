"""Query to find one Application."""

from dataclasses import dataclass

from st_server.shared.application.query import Query


@dataclass(frozen=True)
class FindOneApplicationQuery(Query):
    """Query to find one Application."""

    id: str
