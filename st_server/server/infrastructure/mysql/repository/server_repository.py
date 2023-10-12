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


def _build_filter(filter: dict):
    """Builds the filter."""
    for attr, criteria in filter.items():
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


def _build_sort(sort: list[dict]):
    """Builds the sort."""
    for criteria in sort:
        for attr, order in criteria.items():
            if hasattr(ServerDbModel, attr):
                return getattr(getattr(ServerDbModel, attr), order)()


class ServerRepositoryImpl(ServerRepository):
    """Server repository implementation.

    Repositories are responsible for retrieving and storing aggregates.

    In the `find_many` method, the `filter` parameter is a dictionary that
    contains the filter criteria. The `and_filter` and `or_filter` parameters
    are lists of dictionaries that contain the filter criteria. The `sort`
    parameter is a list of dictionaries that contain the sort criteria.

    The `filter`, `and_filter` and `or_filter` parameters are
    dictionaries with the following structure:

    {
        "attribute": {
            "operator": "value"
        }
    }

    The `attribute` is the name of the attribute to filter by. The `operator`
    is the operator to filter by. The `value` is the value to filter by. The
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

    The `sort` parameter is a list of dictionaries with the following
    structure:

    {
        "attribute": "order"
    }

    The `attribute` is the name of the attribute to sort by. The `order` is the
    order to sort by. The following orders are supported:

    - `asc`: ascending
    - `desc`: descending

    The `limit` parameter is the maximum number of records to return. The
    `offset` parameter is the number of records to skip.

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
        limit: int | None = None,
        offset: int | None = None,
        filter: dict | None = None,
        and_filter: list[dict] | None = None,
        or_filter: list[dict] | None = None,
        sort: list[dict] | None = None,
    ) -> RepositoryPageDto:
        """Returns servers."""
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
            query = session.query(ServerDbModel)
            if filter:
                query = query.filter(_build_filter(filter=filter))
            if and_filter:
                query = query.filter(
                    and_(*[_build_filter(_and) for _and in and_filter])
                )
            if or_filter:
                query = query.filter(
                    or_(*[_build_filter(_or) for _or in or_filter])
                )
            if sort:
                query = query.order_by(_build_sort(sort=sort))
            total = query.count()
            query = query.limit(limit=limit or total)
            query = query.offset(offset=offset)
            users = query.all()
            return RepositoryPageDto(
                total=total,
                items=[
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
