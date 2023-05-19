"""Application repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

from st_server.context.server.domain.application.application import Application
from st_server.context.server.infrastructure.mysql.application.application import (
    ApplicationDbModel,
)
from st_server.shared.core.repository import FILTER_OPERATOR_MAPPER, Repository
from st_server.shared.core.response import RepositoryResponse


class ApplicationRepository(Repository):
    """Application repository implementation."""

    def __init__(self, session: Session) -> None:
        """Application repository.

        Args:
            session (`Session`): SQLAlchemy session object.
        """
        self._session = session

    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        fields: list[str] | None = None,
        **kwargs,
    ) -> RepositoryResponse:
        """Returns all Applications that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no Applications will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all Applications will be returned.

        Args:
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): Offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.

        Returns:
            `RepositoryResponse`: Applications found.
        """
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
                if kwargs and attr.key in kwargs:
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
            query = query.limit(limit or total)
            query = query.offset(((offset or 1) - 1) * (limit or total))
            applications = query.all()

            return RepositoryResponse(
                total_items=total,
                items=[
                    Application.from_dict(application.to_dict(exclude=exclude))
                    for application in applications
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> Application | None:
        """Returns the Application that matches the provided id.

        If no Applications match, the value `None` is returned.

        Args:
            id (`int`): Application id.
            fields (`list[str]`): List of fields to return. Defaults to `None`.

        Returns:
            `Application` | `None`: Application found.
        """
        with self._session as session:
            query = session.query(ApplicationDbModel).filter(
                ApplicationDbModel.id == id
            )

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

            application = query.one_or_none()

            return (
                Application.from_dict(application.to_dict(exclude=exclude))
                if application
                else None
            )

    def add_one(self, aggregate: Application) -> None:
        """Adds the provided Application.

        Args:
            aggregate (`Application`): Application to add.
        """
        with self._session as session:
            model = ApplicationDbModel.from_dict(aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: Application) -> None:
        """Updates the provided Application.

        Args:
            aggregate (`Application`): Application to update.
        """
        with self._session as session:
            model = ApplicationDbModel.from_dict(aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes the Application that matches the provided id.

        Args:
            id (`int`): Application id.
        """
        with self._session as session:
            model = session.get(entity=ApplicationDbModel, ident=id)
            session.delete(model)
            session.commit()
