"""Server repository implementation."""

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from st_server.server.domain.server.server import Server
from st_server.server.domain.server.server_repository import (
    FILTER_OPERATOR_MAPPER,
    ServerRepository,
)
from st_server.shared.domain.repository_response import RepositoryResponse


def _build_filter(filter: dict):
    for attr, criteria in filter.items():
        if hasattr(Server, attr):
            for op, val in criteria.items():
                if isinstance(val, dict):
                    for k, v in val.items():
                        return (
                            func.json_extract(
                                getattr(Server, attr),
                                f"$.{k}",
                            )
                            == v
                        )
                else:
                    return FILTER_OPERATOR_MAPPER[op](
                        Server,
                        attr,
                        val,
                    )


def _build_sort(sort: list[dict]):
    for criteria in sort:
        for attr, order in criteria.items():
            if hasattr(Server, attr):
                return getattr(getattr(Server, attr), order)()


class ServerRepositoryImpl(ServerRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        filter: dict | None = None,
        and_filter: list[dict] | None = None,
        or_filter: list[dict] | None = None,
        sort: list[dict] | None = None,
    ) -> RepositoryResponse:
        if limit is None:
            limit = 0
        if offset is None:
            offset = 0
        if filter is None:
            filter = {}
        if and_filter is None:
            and_filter = []
        if or_filter is None:
            or_filter = []
        if sort is None:
            sort = []
        with self._session as session:
            query = session.query(Server)
            if filter:
                query = query.filter(_build_filter(filter))
            if and_filter:
                query = query.filter(
                    and_(*[_build_filter(_and) for _and in and_filter])
                )
            if or_filter:
                query = query.filter(
                    or_(*[_build_filter(_or) for _or in or_filter])
                )
            if sort:
                query = query.order_by(_build_sort(sort))
            total = query.count()
            query = query.limit(limit or total)
            query = query.offset(offset)
            servers = query.all()
            return RepositoryResponse(total=total, items=servers)

    def find_by_id(self, id: int) -> Server | None:
        with self._session as session:
            return session.get(Server, id)

    def add(self, aggregate: Server) -> None:
        with self._session as session:
            session.add(aggregate)
            session.commit()

    def update(self, aggregate: Server) -> None:
        with self._session as session:
            session.merge(aggregate)
            session.commit()

    def delete_by_id(self, id: int) -> None:
        with self._session as session:
            server = session.get(Server, id)
            if server is not None:
                session.delete(server)
            session.commit()
