"""Environment repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

from st_server.context.server.domain.environment.environment import Environment
from st_server.context.server.infrastructure.mysql.environment.environment import (
    EnvironmentDbModel,
)
from st_server.shared.core.repository import FILTER_OPERATOR_MAPPER, Repository
from st_server.shared.core.response import RepositoryResponse


class EnvironmentRepository(Repository):
    """Environment repository implementation."""

    def __init__(self, session: Session) -> None:
        """Environment repository.

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
        """Returns all environments that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no environments will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all environments will be returned.

        Args:
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): Offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.

        Returns:
            `RepositoryResponse`: Environments found.
        """
        with self._session as session:
            query = session.query(EnvironmentDbModel)

            exclude = []
            for attr in inspect(EnvironmentDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))

                # If the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(EnvironmentDbModel, attr.key))
                        )

                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))

                # If the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)

                # If the attribute is in the kwargs, filter by it.
                if kwargs and attr.key in kwargs:
                    op, val = kwargs[attr.key].split(":")
                    query = query.filter(
                        FILTER_OPERATOR_MAPPER[op](
                            EnvironmentDbModel, attr.key, val
                        )
                    )

                # If the attribute is in the sort criteria, sort by it.
                if sort and attr.key in sort:
                    attr, direction = sort.split(":")
                    sorting = getattr(
                        getattr(EnvironmentDbModel, attr), direction
                    )
                    query = query.order_by(sorting())

            total = query.count()
            query = query.limit(limit or total)
            query = query.offset(((offset or 1) - 1) * (limit or total))
            applications = query.all()

            return RepositoryResponse(
                total_items=total,
                items=[
                    Environment.from_dict(application.to_dict(exclude=exclude))
                    for application in applications
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> Environment | None:
        """Returns the environment that matches the provided id.

        If no environments match, the value `None` is returned.

        Args:
            id (`int`): Environment id.
            fields (`list[str]`): List of fields to return. Defaults to `None`.

        Returns:
            `Environment` | `None`: Environment found.
        """
        with self._session as session:
            query = session.query(EnvironmentDbModel).filter(
                EnvironmentDbModel.id == id
            )

            exclude = []
            for attr in inspect(EnvironmentDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))

                # If the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(getattr(EnvironmentDbModel, attr.key))
                        )

                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))

                # If the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)

            application = query.one_or_none()

            return (
                Environment.from_dict(application.to_dict(exclude=exclude))
                if application
                else None
            )

    def add_one(self, aggregate: Environment) -> None:
        """Adds the provided environment.

        Args:
            aggregate (`Environment`): Environment to add.
        """
        with self._session as session:
            model = EnvironmentDbModel.from_dict(aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: Environment) -> None:
        """Updates the provided environment.

        Args:
            aggregate (`Environment`): Environment to update.
        """
        with self._session as session:
            model = EnvironmentDbModel.from_dict(aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes the environment that matches the provided id.

        Args:
            id (`int`): Environment id.
        """
        with self._session as session:
            model = session.get(entity=EnvironmentDbModel, ident=id)
            session.delete(model)
            session.commit()
