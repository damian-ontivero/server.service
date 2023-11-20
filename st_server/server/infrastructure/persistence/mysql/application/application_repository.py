"""Application repository implementation."""

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session
from st_core.domain.repository_response import RepositoryResponse

from st_server.server.domain.application.application import Application
from st_server.server.domain.application.application_factory import (
    ApplicationFactory,
)
from st_server.server.domain.application.application_repository import (
    FILTER_OPERATOR_MAPPER,
    ApplicationRepository,
)
from st_server.server.infrastructure.persistence.mysql.application.application import (
    ApplicationDbModel,
)


def _build_filter(filter: dict):
    """Builds the filter."""
    for attr, criteria in filter.items():
        if hasattr(ApplicationDbModel, attr):
            for op, val in criteria.items():
                if isinstance(val, dict):
                    for k, v in val.items():
                        return (
                            func.json_extract(
                                getattr(ApplicationDbModel, attr),
                                f"$.{k}",
                            )
                            == v
                        )
                else:
                    return FILTER_OPERATOR_MAPPER[op](
                        ApplicationDbModel,
                        attr,
                        val,
                    )


def _build_sort(sort: list[dict]):
    """Builds the sort."""
    for criteria in sort:
        for attr, order in criteria.items():
            if hasattr(ApplicationDbModel, attr):
                return getattr(getattr(ApplicationDbModel, attr), order)()


class ApplicationRepositoryImpl(ApplicationRepository):
    """Application repository implementation.

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
    ) -> RepositoryResponse:
        """Returns applications."""
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
            query = session.query(ApplicationDbModel)
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
            applications = query.all()
            return RepositoryResponse(
                total=total,
                items=[
                    ApplicationFactory.rebuild(
                        id=application.id,
                        name=application.name,
                        version=application.version,
                        architect=application.architect,
                        discarded=application.discarded,
                    )
                    for application in applications
                ],
            )

    def find_one(self, id: int) -> Application | None:
        """Returns an Application."""
        with self._session as session:
            application = session.get(entity=ApplicationDbModel, ident=id)
            if application is not None:
                return ApplicationFactory.rebuild(
                    id=application.id,
                    name=application.name,
                    version=application.version,
                    architect=application.architect,
                    discarded=application.discarded,
                )

    def save_one(self, aggregate: Application) -> None:
        """Saves an Application."""
        with self._session as session:
            model = session.get(
                entity=ApplicationDbModel, ident=aggregate.id.value
            )
            if model is None:
                model = ApplicationDbModel.from_entity(aggregate)
                session.add(model)
            else:
                model.update(aggregate)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes an Application."""
        with self._session as session:
            application = session.get(entity=ApplicationDbModel, ident=id)
            if application is not None:
                session.delete(application)
                session.commit()
