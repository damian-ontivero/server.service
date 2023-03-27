"""Application service."""

import math

from st_server.domain.application import (
    Application,
    ApplicationAbstractService,
    ApplicationCreate,
    ApplicationNameAlreadyExists,
    ApplicationNotFound,
    ApplicationUpdate,
)
from st_server.domain.helper import ServiceResponse
from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.application.application_repository import (
    ApplicationRepository,
)


class ApplicationService(ApplicationAbstractService):
    """Application service."""

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
        repo = ApplicationRepository(session=sess, model=Application)
        applications = repo.find_many(
            limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = applications.total_items

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
            items=applications.items,
        )

    @classmethod
    # @AuthService.access_token_required
    def find_one(
        cls, id_: int, access_token: str | None = None
    ) -> Application:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `ApplicationNotFound`: No entity found with the provided id.

        Returns:
            `Application`: Entity found.
        """
        sess = cls._session_factory()
        repo = ApplicationRepository(session=sess, model=Application)
        application = repo.find_one(id=id_)

        if application is None:
            raise ApplicationNotFound(id=id_)

        return application

    @classmethod
    # @AuthService.access_token_required
    def add_one(
        cls,
        application_dto: ApplicationCreate,
        access_token: str | None = None,
    ) -> Application:
        """Adds an entity.

        Args:
            application_dto (`ApplicationCreate`): Entity to add.

        Raises:
            `ApplicationNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `Application`: Entity added.
        """
        sess = cls._session_factory()
        repo = ApplicationRepository(session=sess, model=Application)

        if repo.find_many(
            name="eq:{}".format(application_dto.name)
        ).total_items:
            raise ApplicationNameAlreadyExists(email=application_dto.name)

        application = repo.add_one(entity=application_dto)

        return application

    @classmethod
    # @AuthService.access_token_required
    def update_one(
        cls,
        id_: int,
        application_dto: ApplicationUpdate,
        access_token: str | None = None,
    ) -> Application:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            application_dto (`ApplicationUpdate`): Entity to update.

        Raises:
            `ApplicationNotFound`: No entity found with the provided id.

        Returns:
            `Application`: Entity updated.
        """
        sess = cls._session_factory()
        repo = ApplicationRepository(session=sess, model=Application)

        if repo.find_one(id=id_) is None:
            raise ApplicationNotFound(id=id_)

        application = repo.update_one(entity=application_dto)

        return application

    @classmethod
    # @AuthService.access_token_required
    def delete_one(
        cls, id_: int, access_token: str | None = None
    ) -> Application:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.

        Raises:
            `ApplicationNotFound`: No entity found with the provided id.

        Returns:
            `Application`: Entity deleted.
        """
        sess = cls._session_factory()
        repo = ApplicationRepository(session=sess, model=Application)
        application = repo.find_one(id=id_)

        if application is None:
            raise ApplicationNotFound(id=id_)

        application = repo.delete_one(entity=application)

        return application
