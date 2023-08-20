"""Application repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

from st_server.server.domain.entities.application import Application
from st_server.server.domain.repositories.application_repository import (
    FILTER_OPERATOR_MAPPER,
    ApplicationRepository,
)
from st_server.server.infrastructure.mysql.models.application import (
    ApplicationDbModel,
)
from st_server.shared.domain.repositories.repository_page_dto import (
    RepositoryPageDto,
)


class ApplicationRepositoryImpl(ApplicationRepository):
    """Application repository implementation.

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
        """Initialize the repository."""
        self._session = session

    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        fields: list[str] | None = None,
        **kwargs,
    ) -> RepositoryPageDto:
        """Returns Applications."""
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
            query = session.query(ApplicationDbModel)
            exclude = []
            for attr in inspect(ApplicationDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))
                # Else if the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(ApplicationDbModel, attr.key))
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
                            ApplicationDbModel, attr.key, val
                        )
                    )
            # If the attribute is in the sort criteria, sort by it.
            for criteria in sort:
                attr, direction = criteria.split(":")
                sorting = getattr(getattr(ApplicationDbModel, attr), direction)
                query = query.order_by(sorting())
            total = query.count()
            query = query.limit(limit=limit or total)
            query = query.offset(offset=offset)
            applications = query.all()
            return RepositoryPageDto(
                _total=total,
                _items=[
                    Application.from_dict(
                        data=application.to_dict(exclude=exclude)
                    )
                    for application in applications
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> Application | None:
        """Returns an Application."""
        if fields is None:
            fields = []
        with self._session as session:
            query = session.query(ApplicationDbModel).filter(
                ApplicationDbModel.id == id
            )
            exclude = []
            for attr in inspect(ApplicationDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))
                # If the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(ApplicationDbModel, attr.key))
                        )
                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))
                # If the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)
            application = query.one_or_none()
            return (
                Application.from_dict(
                    data=application.to_dict(exclude=exclude)
                )
                if application
                else None
            )

    def add_one(self, aggregate: Application) -> None:
        """Adds an Application."""
        with self._session as session:
            model = ApplicationDbModel.from_dict(data=aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: Application) -> None:
        """Updates an Application."""
        with self._session as session:
            model = ApplicationDbModel.from_dict(data=aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes an Application."""
        with self._session as session:
            model = session.get(entity=ApplicationDbModel, ident=id)
            session.delete(model)
            session.commit()
