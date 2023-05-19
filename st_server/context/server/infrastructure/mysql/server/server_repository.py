"""Server repository implementation."""

from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
    Session,
    joinedload,
    load_only,
)

from st_server.context.server.domain.server.server import Server
from st_server.context.server.infrastructure.mysql.server.server import (
    ServerDbModel,
)
from st_server.shared.core.repository import FILTER_OPERATOR_MAPPER, Repository
from st_server.shared.core.response import RepositoryResponse


class ServerRepository(Repository):
    """Server repository implementation."""

    def __init__(self, session: Session) -> None:
        """Server repository.

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
        """Returns all Servers that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no Servers will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all Servers will be returned.

        Args:
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): Offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.

        Returns:
            `RepositoryResponse`: Servers found.
        """
        with self._session as session:
            query = session.query(ServerDbModel)

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

                # If the attribute is in the kwargs, filter by it.
                if kwargs and attr.key in kwargs:
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
            query = query.limit(limit or total)
            query = query.offset(((offset or 1) - 1) * (limit or total))
            servers = query.all()

            return RepositoryResponse(
                total_items=total,
                items=[
                    Server.from_dict(server.to_dict(exclude=exclude))
                    for server in servers
                ],
            )

    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> Server | None:
        """Returns the Server that matches the provided id.

        If no Servers match, the value `None` is returned.

        Args:
            id (`int`): Server id.
            fields (`list[str]`): List of fields to return. Defaults to `None`.

        Returns:
            `Server` | `None`: Server found.
        """
        with self._session as session:
            query = session.query(ServerDbModel).filter(ServerDbModel.id == id)

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

            server = query.one_or_none()

            return (
                Server.from_dict(server.to_dict(exclude=exclude))
                if server
                else None
            )

    def add_one(self, aggregate: Server) -> None:
        """Adds the provided Server.

        Args:
            aggregate (`Server`): Server to add.
        """
        with self._session as session:
            model = ServerDbModel.from_dict(aggregate.to_dict())
            session.add(model)
            session.commit()

    def update_one(self, aggregate: Server) -> None:
        """Updates the provided Server.

        Args:
            aggregate (`Server`): Server to update.
        """
        with self._session as session:
            model = ServerDbModel.from_dict(aggregate.to_dict())
            session.merge(model)
            session.commit()

    def delete_one(self, id: int) -> None:
        """Deletes the Server that matches the provided id.

        Args:
            id (`int`): Server id.
        """
        with self._session as session:
            model = session.get(entity=ServerDbModel, ident=id)
            session.delete(model)
            session.commit()
