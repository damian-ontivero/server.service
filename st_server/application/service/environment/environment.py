"""Environment service."""

import math

from st_server.domain.environment import (
    Environment,
    EnvironmentAbstractService,
    EnvironmentCreate,
    EnvironmentNameAlreadyExists,
    EnvironmentNotFound,
    EnvironmentUpdate,
)
from st_server.domain.helper import ServiceResponse
from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.environment.environment_repository import (
    EnvironmentRepository,
)


class EnvironmentService(EnvironmentAbstractService):
    """Environment service."""

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
        repo = EnvironmentRepository(session=sess, model=Environment)
        environments = repo.find_many(
            limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = environments.total_items

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
            items=environments.items,
        )

    @classmethod
    # @AuthService.access_token_required
    def find_one(
        cls, id_: int, access_token: str | None = None
    ) -> Environment:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `EnvironmentNotFound`: No entity found with the provided id.

        Returns:
            `Environment`: Entity found.
        """
        sess = cls._session_factory()
        repo = EnvironmentRepository(session=sess, model=Environment)
        environment = repo.find_one(id=id_)

        if environment is None:
            raise EnvironmentNotFound(id=id_)

        return environment

    @classmethod
    # @AuthService.access_token_required
    def add_one(
        cls,
        environment_dto: EnvironmentCreate,
        access_token: str | None = None,
    ) -> Environment:
        """Adds an entity.

        Args:
            environment_dto (`EnvironmentCreate`): Entity to add.

        Raises:
            `EnvironmentNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `Environment`: Entity added.
        """
        sess = cls._session_factory()
        repo = EnvironmentRepository(session=sess, model=Environment)

        if repo.find_many(
            name="eq:{}".format(environment_dto.name)
        ).total_items:
            raise EnvironmentNameAlreadyExists(name=environment_dto.name)

        environment = repo.add_one(entity=environment_dto)

        return environment

    @classmethod
    # @AuthService.access_token_required
    def update_one(
        cls,
        id_: int,
        environment_dto: EnvironmentUpdate,
        access_token: str | None = None,
    ) -> Environment:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            environment_dto (`EnvironmentUpdate`): Entity to update.

        Raises:
            `EnvironmentNotFound`: No entity found with the provided id.

        Returns:
            `Environment`: Entity updated.
        """
        sess = cls._session_factory()
        repo = EnvironmentRepository(session=sess, model=Environment)

        if repo.find_one(id=id_) is None:
            raise EnvironmentNotFound(id=id_)

        environment = repo.update_one(entity=environment_dto)

        return environment

    @classmethod
    # @AuthService.access_token_required
    def delete_one(
        cls, id_: int, access_token: str | None = None
    ) -> Environment:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `EnvironmentNotFound`: No entity found with the provided id.

        Returns:
            `Environment`: Entity deleted.
        """
        sess = cls._session_factory()
        repo = EnvironmentRepository(session=sess, model=Environment)
        environment = repo.find_one(id=id_)

        if environment is None:
            raise EnvironmentNotFound(id=id_)

        environment = repo.delete_one(entity=environment)

        return environment
