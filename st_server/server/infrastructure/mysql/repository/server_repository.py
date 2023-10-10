"""Server repository implementation."""

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from st_server.server.domain.entity.server import Server
from st_server.server.domain.repository.server_repository import (
    FILTER_OPERATOR_MAPPER,
    ServerRepository,
)
from st_server.server.infrastructure.mysql.model.server import ServerDbModel
from st_server.shared.domain.repository.repository_page_dto import (
    RepositoryPageDto,
)


def _build_filter(_filter: dict):
    """Builds the _filter."""
    for attr, criteria in _filter.items():
        if hasattr(ServerDbModel, attr):
            for op, val in criteria.items():
                if isinstance(val, dict):
                    for k, v in val.items():
                        return (
                            func.json_extract(
                                getattr(ServerDbModel, attr),
                                f"$.{k}",
                            )
                            == v
                        )
                else:
                    return FILTER_OPERATOR_MAPPER[op](
                        ServerDbModel,
                        attr,
                        val,
                    )


def _build_sort(_sort: list[dict]):
    """Builds the _sort."""
    for criteria in _sort:
        for attr, order in criteria.items():
            if hasattr(ServerDbModel, attr):
                return getattr(getattr(ServerDbModel, attr), order)()


class ServerRepositoryImpl(ServerRepository):
    """Server repository implementation.

    Repositories are responsible for retrieving and storing aggregates.

    In the `find_many` method, the `_filter` parameter is a dictionary that
    contains the _filter criteria. The `_and_filter` and `_or_filter` parameters
    are lists of dictionaries that contain the _filter criteria. The `_sort`
    parameter is a list of dictionaries that contain the _sort criteria.

    The `_filter`, `_and_filter` and `_or_filter` parameters are
    dictionaries with the following structure:

    {
        "attribute": {
            "operator": "value"
        }
    }

    The `attribute` is the name of the attribute to _filter by. The `operator`
    is the operator to _filter by. The `value` is the value to _filter by. The
    following operators are supported:

    - `eq`: equal to
    - `gt`: greater than
    - `ge`: greater than or equal to
    - `lt`: less than
    - `le`: less than or equal to
    - `in`: in
    - `btw`: between
    - `lk`: ilike

    The `in` operator expects a comma-separated list of values. The `btw`
    operator expects a comma-separated list of two values.

    The `_sort` parameter is a list of dictionaries with the following
    structure:

    {
        "attribute": "order"
    }

    The `attribute` is the name of the attribute to _sort by. The `order` is the
    order to _sort by. The following orders are supported:

    - `asc`: ascending
    - `desc`: descending

    The `_limit` parameter is the maximum number of records to return. The
    `_offset` parameter is the number of records to skip.

    The `find_one` method returns a single aggregate. The `id` parameter is the
    ID of the aggregate to return.

    The `save_one` method adds a single aggregate. The `aggregate` parameter is
    the aggregate to add.

    The `save_one` method updates a single aggregate. The `aggregate`
    parameter is the aggregate to update.

    The `delete_one` method deletes a single aggregate. The `id` parameter is
    the ID of the aggregate to delete.
    """

    def __init__(self, session: Session) -> None:
        """Initializes the repository."""
        self._session = session

    def find_many(
        self,
        _limit: int | None = None,
        _offset: int | None = None,
        _filter: dict | None = None,
        _and_filter: list[dict] | None = None,
        _or_filter: list[dict] | None = None,
        _sort: list[dict] | None = None,
    ) -> RepositoryPageDto:
        """Returns servers."""
        if _limit is None:
            _limit = 0
        if _offset is None:
            _offset = 0
        if _filter is None:
            _filter = {}
        if _and_filter is None:
            _and_filter = []
        if _or_filter is None:
            _or_filter = []
        if _sort is None:
            _sort = []
        with self._session as session:
            query = session.query(ServerDbModel)
            if _filter:
                query = query.filter(_build_filter(_filter=_filter))
            if _and_filter:
                query = query.filter(
                    and_(*[_build_filter(_and) for _and in _and_filter])
                )
            if _or_filter:
                query = query.filter(
                    or_(*[_build_filter(_or) for _or in _or_filter])
                )
            if _sort:
                query = query.order_by(_build_sort(_sort=_sort))
            total = query.count()
            query = query.limit(limit=_limit or total)
            query = query.offset(offset=_offset)
            users = query.all()
            return RepositoryPageDto(
                _total=total,
                _items=[
                    Server.from_dict(data=user.to_dict()) for user in users
                ],
            )

    def find_one(self, id: int) -> Server | None:
        """Returns a server."""
        with self._session as session:
            user = session.get(entity=ServerDbModel, ident=id)
            return Server.from_dict(data=user.to_dict()) if user else None

    def save_one(self, aggregate: Server) -> None:
        """Saves a server."""
        with self._session as session:
            model = session.get(entity=ServerDbModel, ident=aggregate.id.value)
            if model is None:
                model = ServerDbModel.from_dict(data=aggregate.to_dict())
                session.add(model)
            else:
                model.update(data=aggregate.to_dict())
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes a server."""
        with self._session as session:
            session.query(ServerDbModel).filter(
                ServerDbModel.id == id
            ).delete()
            session.commit()
