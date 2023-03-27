"""Operating System service."""

import math

from st_server.domain.helper import ServiceResponse
from st_server.domain.operating_system import (
    OperatingSystem,
    OperatingSystemAbstractService,
    OperatingSystemCreate,
    OperatingSystemNameAlreadyExists,
    OperatingSystemNotFound,
    OperatingSystemUpdate,
)
from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.operating_system.operating_system_repository import (
    OperatingSystemRepository,
)


class OperatingSystemService(OperatingSystemAbstractService):
    """Operating System service."""

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
        repo = OperatingSystemRepository(session=sess, model=OperatingSystem)
        operating_systems = repo.find_many(
            limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = operating_systems.total_items

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
            items=operating_systems.items,
        )

    @classmethod
    # @AuthService.access_token_required
    def find_one(
        cls, id_: int, access_token: str | None = None
    ) -> OperatingSystem:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `OperatingSystemNotFound`: No entity found with the provided id.

        Returns:
            `OperatingSystem`: Entity found.
        """
        sess = cls._session_factory()
        repo = OperatingSystemRepository(session=sess, model=OperatingSystem)
        operating_system = repo.find_one(id=id_)

        if operating_system is None:
            raise OperatingSystemNotFound(id=id_)

        return operating_system

    @classmethod
    # @AuthService.access_token_required
    def add_one(
        cls,
        operating_system_dto: OperatingSystemCreate,
        access_token: str | None = None,
    ) -> OperatingSystem:
        """Adds an entity.

        Args:
            operating_system_dto (`OperatingSystemCreate`): Entity to add.

        Raises:
            `OperatingSystemNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `OperatingSystem`: Entity added.
        """
        sess = cls._session_factory()
        repo = OperatingSystemRepository(session=sess, model=OperatingSystem)

        if repo.find_many(
            name="eq:{}".format(operating_system_dto.name)
        ).total_items:
            raise OperatingSystemNameAlreadyExists(
                name=operating_system_dto.name
            )

        operating_system = repo.add_one(entity=operating_system_dto)

        return operating_system

    @classmethod
    # @AuthService.access_token_required
    def update_one(
        cls,
        id_: int,
        operating_system_dto: OperatingSystemUpdate,
        access_token: str | None = None,
    ) -> OperatingSystem:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            operating_system_dto (`OperatingSystemUpdate`): Entity to update.

        Raises:
            `OperatingSystemNotFound`: No entity found with the provided id.

        Returns:
            `OperatingSystem`: Entity updated.
        """
        sess = cls._session_factory()
        repo = OperatingSystemRepository(session=sess, model=OperatingSystem)

        if repo.find_one(id=id_) is None:
            raise OperatingSystemNotFound(id=id_)

        operating_system = repo.update_one(entity=operating_system_dto)

        return operating_system

    @classmethod
    # @AuthService.access_token_required
    def delete_one(
        cls, id_: int, access_token: str | None = None
    ) -> OperatingSystem:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `OperatingSystemNotFound`: No entity found with the provided id.

        Returns:
            `OperatingSystem`: Entity deleted.
        """
        sess = cls._session_factory()
        repo = OperatingSystemRepository(session=sess, model=OperatingSystem)
        operating_system = repo.find_one(id=id_)

        if operating_system is None:
            raise OperatingSystemNotFound(id=id_)

        operating_system = repo.delete_one(entity=operating_system)

        return operating_system
