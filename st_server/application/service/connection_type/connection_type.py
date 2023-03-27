"""Connection Type service."""

import math

from st_server.domain.connection_type import (
    ConnectionType,
    ConnectionTypeAbstractService,
    ConnectionTypeCreate,
    ConnectionTypeNameAlreadyExists,
    ConnectionTypeNotFound,
    ConnectionTypeUpdate,
)
from st_server.domain.helper import ServiceResponse
from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.connection_type.connection_type_repository import (
    ConnectionTypeRepository,
)


class ConnectionTypeService(ConnectionTypeAbstractService):
    """Connection Type service."""

    _session_factory = db.SessionLocal

    @classmethod
    # @AuthService.access_token_required
    # @validate_pagination
    # @validate_sort
    # @validate_filter
    def find_many(
        cls,
        per_page: int | None = None,
        page: int | None = None,
        sort: list[str] | None = None,
        access_token: str | None = None,
        **kwargs,
    ) -> ServiceResponse:
        """Returns all entities that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no entity will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all entities will be returned.

        Args:
            per_page (`int` | `None`, `optional`): Number of records per page. Defaults to `None`.
            page (`int` | `None`, `optional`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`, `optional`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Entities found.
        """
        sess = cls._session_factory()
        repo = ConnectionTypeRepository(session=sess, model=ConnectionType)
        connection_types = repo.find_many(
            limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = connection_types.total_items

        return ServiceResponse(
            per_page=per_page,
            page=(page or 1),
            prev_page=((page or 1) - 1) if (page or 1) > 1 else None,
            next_page=((page or 1) + 1)
            if (page or 1) > 0
            and (page or 1)
            < math.ceil(float(total) / float(per_page or total))
            else None,
            last_page=math.ceil(float(total) / float(per_page or total)),
            first_page=1,
            items=connection_types.items,
        )

    @classmethod
    # @AuthService.access_token_required
    def find_one(
        cls, id_: int, access_token: str | None = None
    ) -> ConnectionType:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `ConnectionTypeNotFound`: No entity found with the provided id.

        Returns:
            `ConnectionType`: Entity found.
        """
        sess = cls._session_factory()
        repo = ConnectionTypeRepository(session=sess, model=ConnectionType)
        connection_type = repo.find_one(id=id_)

        if connection_type is None:
            raise ConnectionTypeNotFound(id=id_)

        return connection_type

    @classmethod
    # @AuthService.access_token_required
    def add_one(
        cls,
        connection_type_dto: ConnectionTypeCreate,
        access_token: str | None = None,
    ) -> ConnectionType:
        """Adds an entity.

        Args:
            connection_type_dto (`ConnectionTypeCreate`): Entity to add.

        Raises:
            `ConnectionTypeNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `ConnectionType`: Entity added.
        """
        sess = cls._session_factory()
        repo = ConnectionTypeRepository(session=sess, model=ConnectionType)

        if repo.find_many(
            name="eq:{}".format(connection_type_dto.name)
        ).total_items:
            raise ConnectionTypeNameAlreadyExists(
                name=connection_type_dto.name
            )

        connection_type = repo.add_one(entity=connection_type_dto)

        return connection_type

    @classmethod
    # @AuthService.access_token_required
    def update_one(
        cls,
        id_: int,
        connection_type_dto: ConnectionTypeUpdate,
        access_token: str | None = None,
    ) -> ConnectionType:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            connection_type_dto (`ConnectionTypeUpdate`): Entity to update.

        Raises:
            `ConnectionTypeNotFound`: No entity found with the provided id.

        Returns:
            `ConnectionType`: Entity updated.
        """
        sess = cls._session_factory()
        repo = ConnectionTypeRepository(session=sess, model=ConnectionType)

        if repo.find_one(id=id_) is None:
            raise ConnectionTypeNotFound(id=id_)

        connection_type = repo.update_one(entity=connection_type_dto)

        return connection_type

    @classmethod
    # @AuthService.access_token_required
    def delete_one(
        cls, id_: int, access_token: str | None = None
    ) -> ConnectionType:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `ConnectionTypeNotFound`: No entity found with the provided id.

        Returns:
            `ConnectionType`: Entity deleted.
        """
        sess = cls._session_factory()
        repo = ConnectionTypeRepository(session=sess, model=ConnectionType)
        connection_type = repo.find_one(id=id_)

        if connection_type is None:
            raise ConnectionTypeNotFound(id=id_)

        connection_type = repo.delete_one(entity=connection_type)

        return connection_type
