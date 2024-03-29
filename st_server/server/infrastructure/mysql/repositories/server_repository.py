"""Server repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

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

    In the `find_many` method, the `fields` parameter is a list of strings with the
    field names to be loaded.

    If a `None` value is provided to limit, there will be no pagination.
    If a `Zero` value is provided to limit, no aggregates will be returned.
    If a `None` value is provided to offset, the first offset will be returned.
    If a `None` value is provided to kwargs, all aggregates will be returned.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        fields: list[str] | None = None,
        **kwargs,
    ) -> RepositoryPageDto:
        if limit is None:
            limit = 0
        if offset is None:
            offset = 0
        if sort is None:
            sort = []
        if fields is None:
            fields = []
        if kwargs is None:
            kwargs = {}
        with self._session as session:
            query = session.query(ServerDbModel)
            exclude = []
            for attr in inspect(ServerDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))
                # Else if the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(ServerDbModel, attr.key))
                        )
                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))
                # Else if the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)
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
                    Server.from_dict(server.to_dict(exclude=exclude))
                    for server in servers
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> Server | None:
        if fields is None:
            fields = []
        with self._session as session:
            query = session.query(ServerDbModel).filter(ServerDbModel.id == id)
            exclude = []
            for attr in inspect(ServerDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))
                # If the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(ServerDbModel, attr.key))
                        )
                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))
                # If the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)
            server = query.one_or_none()
            return (
                Server.from_dict(server.to_dict(exclude=exclude))
                if server
                else None
            )

    def add_one(self, aggregate: Server) -> None:
        with self._session as session:
            model = ServerDbModel.from_dict(aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: Server) -> None:
        with self._session as session:
            model = ServerDbModel.from_dict(aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        with self._session as session:
            model = session.get(entity=ServerDbModel, ident=id)
            session.delete(model)
            session.commit()
