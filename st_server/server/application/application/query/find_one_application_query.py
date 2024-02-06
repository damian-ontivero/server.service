from dataclasses import dataclass

from st_server.shared.domain.bus.query.query import Query


@dataclass(frozen=True)
class FindOneApplicationQuery(Query):
    id: str
