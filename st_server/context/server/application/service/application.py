"""Application service."""

import math

from st_server.context.server.domain.application.application import Application
from st_server.shared.core.exception import AlreadyExists, NotFound
from st_server.shared.core.message_bus import MessageBus
from st_server.shared.core.repository import Repository
from st_server.shared.core.response import ServiceResponse
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort


class ApplicationService:
    """Application service."""

    def __init__(
        self, repository: Repository, message_bus: MessageBus
    ) -> None:
        """Initializes the service.

        Args:
            repository (`Repository`): Application repository.
            message_bus (`MessageBus`): Message bus.
        """
        self._repository = repository
        self._message_bus = message_bus

    # @AuthService.access_token_required
    @validate_pagination
    @validate_sort
    @validate_filter
    def find_many(
        self,
        fields: list[str] | None = None,
        per_page: int | None = None,
        page: int | None = None,
        sort: list[str] | None = None,
        access_token: str | None = None,
        **kwargs,
    ) -> ServiceResponse:
        """Returns all Applications that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no Application will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all Applications will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            per_page (`int` | `None`): Number of records per page. Defaults to `None`.
            page (`int` | `None`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Applications found.
        """
        applications = self._repository.find_many(
            fields=fields, limit=per_page, offset=page, sort=sort, **kwargs
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

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> Application:
        """Returns the Application that matches the provided id.

        Args:
            id (`int`): Application id.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Application found with the provided id.

        Returns:
            `Application`: Application found.
        """
        application = self._repository.find_one(id=id, fields=fields)

        if application is None:
            raise NotFound(message=f"Application with id {id} not found.")

        return application

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> Application:
        """Adds the provided Application and publishes the Application events.

        Args:
            data (`dict`): Dictionary with the Application data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `AlreadyExists`: An Application with the provided name already exists.

        Returns:
            `Application`: Application added.
        """
        application = Application.create(**data)
        applications = self._repository.find_many(
            name="eq:{}".format(application.name)
        )

        if applications.total_items:
            raise AlreadyExists(
                message=f"Application with name {application.name} already exists."
            )

        self._repository.add_one(aggregate=application)
        # self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()

        return self._repository.find_one(id=application.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> Application:
        """Updates the Application that matches the provided id and publishes the events.

        Args:
            id (`str`): Application id.
            data (`dict`): Dictionary with the Application data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Application found with the provided id.
            `AlreadyExists`: A Application with the provided name already exists.

        Returns:
            `Application`: Application updated.
        """
        application = self._repository.find_one(id=id)

        if application is None:
            raise NotFound(message=f"Application with id {id} not found.")

        for key, value in data.items():
            setattr(application, key, value)

        self._repository.update_one(aggregate=application)
        self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()

        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        """Discards the Application that matches the provided id and publishes the events.

        Args:
            id (`str`): Application id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Application found with the provided id.
        """
        application = self._repository.find_one(id=id)

        if application is None:
            raise NotFound(message=f"Application with id {id} not found.")

        application.discard()

        self._repository.update_one(aggregate=application)
        self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        """Deletes the Application that matches the provided id and publishes the events.

        Args:
            id (`str`): Application id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Application found with the provided id.
        """
        application = self._repository.find_one(id=id)

        if application is None:
            raise NotFound(message=f"Application with id {id} not found.")

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()
