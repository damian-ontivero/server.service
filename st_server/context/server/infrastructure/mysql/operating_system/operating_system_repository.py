"""OperatingSystem repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

from st_server.context.server.domain.operating_system.operating_system import (
    OperatingSystem,
)
from st_server.context.server.infrastructure.mysql.operating_system.operating_system import (
    OperatingSystemDbModel,
)
from st_server.shared.core.repository import FILTER_OPERATOR_MAPPER, Repository
from st_server.shared.core.response import RepositoryResponse


class OperatingSystemRepository(Repository):
    """OperatingSystem repository implementation."""

    def __init__(self, session: Session) -> None:
        """OperatingSystem repository.

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
        """Returns all OperatingSystems that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no OperatingSystems will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all OperatingSystems will be returned.

        Args:
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): Offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.

        Returns:
            `RepositoryResponse`: OperatingSystems found.
        """
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
            query = session.query(OperatingSystemDbModel)

            exclude = []
            for attr in inspect(OperatingSystemDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))

                # Else if the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(
                                getattr(OperatingSystemDbModel, attr.key)
                            )
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
                            OperatingSystemDbModel, attr.key, val
                        )
                    )

            # If the attribute is in the sort criteria, sort by it.
            for criteria in sort:
                attr, direction = criteria.split(":")
                sorting = getattr(
                    getattr(OperatingSystemDbModel, attr), direction
                )
                query = query.order_by(sorting())

            total = query.count()
            query = query.limit(limit=limit or total)
            query = query.offset(offset=offset)
            users = query.all()

            return RepositoryResponse(
                total_items=total,
                items=[
                    OperatingSystem.from_dict(user.to_dict(exclude=exclude))
                    for user in users
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> OperatingSystem | None:
        """Returns the OperatingSystem that matches the provided id.

        If no OperatingSystems match, the value `None` is returned.

        Args:
            id (`int`): OperatingSystem id.
            fields (`list[str]`): List of fields to return. Defaults to `None`.

        Returns:
            `OperatingSystem` | `None`: OperatingSystem found.
        """
        if fields is None:
            fields = []

        with self._session as session:
            query = session.query(OperatingSystemDbModel).filter(
                OperatingSystemDbModel.id == id
            )

            exclude = []
            for attr in inspect(OperatingSystemDbModel).attrs:
                # If no fields are provided, load all.
                if not fields:
                    query = query.options(joinedload("*"))

                # If the attribute is in the fields, load it.
                elif attr.key in fields:
                    if isinstance(attr, ColumnProperty):
                        query = query.options(
                            load_only(
                                getattr(OperatingSystemDbModel, attr.key)
                            )
                        )

                    if isinstance(attr, RelationshipProperty):
                        query = query.options(joinedload(attr))

                # If the attribute is not in the fields, exclude it.
                else:
                    exclude.append(attr.key)

            user = query.one_or_none()

            return (
                OperatingSystem.from_dict(user.to_dict(exclude=exclude))
                if user
                else None
            )

    def add_one(self, aggregate: OperatingSystem) -> None:
        """Adds the provided OperatingSystem.

        Args:
            aggregate (`OperatingSystem`): OperatingSystem to add.
        """
        with self._session as session:
            model = OperatingSystemDbModel.from_dict(aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: OperatingSystem) -> None:
        """Updates the provided OperatingSystem.

        Args:
            aggregate (`OperatingSystem`): OperatingSystem to update.
        """
        with self._session as session:
            model = OperatingSystemDbModel.from_dict(aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes the OperatingSystem that matches the provided id.

        Args:
            id (`int`): OperatingSystem id.
        """
        with self._session as session:
            model = session.get(entity=OperatingSystemDbModel, ident=id)
            session.delete(model)
            session.commit()
