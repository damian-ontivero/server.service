from dataclasses import dataclass

from st_server.shared.domain.bus.query.query import Query


@dataclass(frozen=True)
class FindOneServerQuery(Query):
    id: str
