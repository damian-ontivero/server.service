"""ConnectionType repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

from st_server.context.server.domain.entity.connection_type import (
    ConnectionType,
)
from st_server.context.server.infrastructure.mysql.model.connection_type import (
    ConnectionTypeDbModel,
)
from st_server.shared.core.repository import FILTER_OPERATOR_MAPPER, Repository
from st_server.shared.core.response import RepositoryResponse


class ConnectionTypeRepository(Repository):
    """ConnectionType repository implementation.

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
    ) -> RepositoryResponse:
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
            query = session.query(ConnectionTypeDbModel)
            exclude = []
            for attr in inspect(ConnectionTypeDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))
                # Else if the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(ConnectionTypeDbModel, attr.key))
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
                            ConnectionTypeDbModel, attr.key, val
                        )
                    )
            # If the attribute is in the sort criteria, sort by it.
            for criteria in sort:
                attr, direction = criteria.split(":")
                sorting = getattr(
                    getattr(ConnectionTypeDbModel, attr), direction
                )
                query = query.order_by(sorting())
            total = query.count()
            query = query.limit(limit=limit or total)
            query = query.offset(offset=offset)
            users = query.all()
            return RepositoryResponse(
                total_items=total,
                items=[
                    ConnectionType.from_dict(user.to_dict(exclude=exclude))
                    for user in users
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> ConnectionType | None:
        if fields is None:
            fields = []
        with self._session as session:
            query = session.query(ConnectionTypeDbModel).filter(
                ConnectionTypeDbModel.id == id
            )
            exclude = []
            for attr in inspect(ConnectionTypeDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))
                # If the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(ConnectionTypeDbModel, attr.key))
                        )
                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))
                # If the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)
            user = query.one_or_none()
            return (
                ConnectionType.from_dict(user.to_dict(exclude=exclude))
                if user
                else None
            )

    def add_one(self, aggregate: ConnectionType) -> None:
        with self._session as session:
            model = ConnectionTypeDbModel.from_dict(aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: ConnectionType) -> None:
        with self._session as session:
            model = ConnectionTypeDbModel.from_dict(aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        with self._session as session:
            model = session.get(entity=ConnectionTypeDbModel, ident=id)
            session.delete(model)
            session.commit()
