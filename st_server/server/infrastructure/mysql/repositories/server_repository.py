"""Server repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from st_server.server.domain.entities.server import Server
from st_server.server.domain.repositories.server_repository import (
    FILTER_OPERATOR_MAPPER,
    ServerRepository,
)
from st_server.server.infrastructure.mysql.models.server import ServerDbModel
from st_server.shared.domain.repositories.repository_page_dto import (
    RepositoryPageDto,
)


class ServerRepositoryImpl(ServerRepository):
    """Server repository implementation.

    Repositories are responsible for retrieving and storing aggregates.

    In the `find_many` method, the `kwargs` parameter is a dictionary of filters. The
    key is the field name and the value is a string with the filter operator and
    the value separated by a colon.

    The available filter operators are:
    - `eq`: equal
    - `gt`: greater than
    - `ge`: greater than or equal
    - `lt`: less than
    - `le`: less than or equal
    - `in`: in
    - `btw`: between
    - `lk`: like

        Example: `{"name": "lk:John"}`

    In the `find_many` method, the `sort` parameter is a list of strings with the
    field name and the sort criteria separated by a colon.

    The available sort criteria are:
    - asc: ascending
    - desc: descending

        Example: `["name:asc", "age:desc"]`

    If a `None` value is provided to limit, there will be no pagination.
    If a `Zero` value is provided to limit, no aggregates will be returned.
    If a `None` value is provided to offset, the first offset will be returned.
    If a `None` value is provided to kwargs, all aggregates will be returned.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the repository."""
        self._session = session

    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        **kwargs,
    ) -> RepositoryPageDto:
        """Returns Servers."""
        if limit is None:
            limit = 0
        if offset is None:
            offset = 0
        if sort is None:
            sort = []
        if kwargs is None:
            kwargs = {}
        with self._session as session:
            query = session.query(ServerDbModel)
            for attr in inspect(ServerDbModel).attrs:
                # If the attribute is in the kwargs, filter by it.
                if attr.key in kwargs:
                    op, val = kwargs[attr.key].split(":")
                    query = query.filter(
                        FILTER_OPERATOR_MAPPER[op](
                            ServerDbModel, attr.key, val
                        )
                    )
            # If the attribute is in the sort criteria, sort by it.
            for criteria in sort:
                attr, direction = criteria.split(":")
                sorting = getattr(getattr(ServerDbModel, attr), direction)
                query = query.order_by(sorting())
            total = query.count()
            query = query.limit(limit=limit or total)
            query = query.offset(offset=offset)
            servers = query.all()
            return RepositoryPageDto(
                _total=total,
                _items=[
                    Server.from_dict(data=server.to_dict())
                    for server in servers
                ],
            )

    def find_one(self, id: int) -> Server | None:
        """Returns a Server."""
        with self._session as session:
            query = session.query(ServerDbModel).filter(ServerDbModel.id == id)
            server = query.one_or_none()
            return Server.from_dict(data=server.to_dict()) if server else None

    def add_one(self, aggregate: Server) -> None:
        """Adds a Server."""
        with self._session as session:
            model = ServerDbModel.from_dict(data=aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: Server) -> None:
        """Updates a Server."""
        with self._session as session:
            model = ServerDbModel.from_dict(data=aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes a Server."""
        with self._session as session:
            model = session.get(entity=ServerDbModel, ident=id)
            session.delete(model)
            session.commit()
