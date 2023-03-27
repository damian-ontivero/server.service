"""Server service."""

import math

from st_server.domain.helper import ServiceResponse
from st_server.domain.server import (
    Server,
    ServerAbstractService,
    ServerCreate,
    ServerNameAlreadyExists,
    ServerNotFound,
    ServerUpdate,
)
from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.server.server_repository import (
    ServerRepository,
)


class ServerService(ServerAbstractService):
    """Server service."""

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
        repo = ServerRepository(session=sess, model=Server)
        servers = repo.find_many(
            limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = servers.total_items

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
            items=servers.items,
        )

    @classmethod
    # @AuthService.access_token_required
    def find_one(cls, id_: int, access_token: str | None = None) -> Server:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `ServerNotFound`: No entity found with the provided id.

        Returns:
            `Server`: Entity found.
        """
        sess = cls._session_factory()
        repo = ServerRepository(session=sess, model=Server)
        server = repo.find_one(id=id_)

        if server is None:
            raise ServerNotFound(id=id_)

        return server

    @classmethod
    # @AuthService.access_token_required
    def add_one(
        cls,
        server_dto: ServerCreate,
        access_token: str | None = None,
    ) -> Server:
        """Adds an entity.

        Args:
            server_dto (`ServerCreate`): Entity to add.

        Raises:
            `ServerNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `Server`: Entity added.
        """
        sess = cls._session_factory()
        repo = ServerRepository(session=sess, model=Server)

        if repo.find_many(name="eq:{}".format(server_dto.name)).total_items:
            raise ServerNameAlreadyExists(name=server_dto.name)

        server = repo.add_one(entity=server_dto)

        return server

    @classmethod
    # @AuthService.access_token_required
    def update_one(
        cls,
        id_: int,
        server_dto: ServerUpdate,
        access_token: str | None = None,
    ) -> Server:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            server_dto (`ServerUpdate`): Entity to update.

        Raises:
            `ServerNotFound`: No entity found with the provided id.

        Returns:
            `Server`: Entity updated.
        """
        sess = cls._session_factory()
        repo = ServerRepository(session=sess, model=Server)

        if repo.find_one(id=id_) is None:
            raise ServerNotFound(id=id_)

        server = repo.update_one(entity=server_dto)

        return server

    @classmethod
    # @AuthService.access_token_required
    def delete_one(cls, id_: int, access_token: str | None = None) -> Server:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `ServerNotFound`: No entity found with the provided id.

        Returns:
            `Server`: Entity deleted.
        """
        sess = cls._session_factory()
        repo = ServerRepository(session=sess, model=Server)
        server = repo.find_one(id=id_)

        if server is None:
            raise ServerNotFound(id=id_)

        server = repo.delete_one(entity=server)

        return server
