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
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        fields: list[str] | None = None,
        access_token: str | None = None,
        **kwargs,
    ) -> ServiceResponse:
        """Returns all Applications that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no Application will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all Applications will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Applications found.
        """
        if fields is None:
            fields = []

        if limit is None:
            limit = 0

        if offset is None:
            offset = 0

        if sort is None:
            sort = []

        if kwargs is None:
            kwargs = {}

        applications = self._repository.find_many(
            limit=limit, offset=offset, sort=sort, fields=fields, **kwargs
        )
        total = applications.total_items

        return ServiceResponse(
            limit=limit,
            offset=(offset or 1),
            prev_offset=((offset or 1) - 1) if (offset or 1) > 1 else None,
            next_offset=((offset or 1) + 1)
            if (offset or 1) > 0
            and (offset or 1) < math.ceil(float(total) / float(limit or total))
            else None,
            last_offset=math.ceil(float(total) / float(limit or total)),
            first_offset=1,
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
        if fields is None:
            fields = []

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
            `AlreadyExists`: An Application with the provided email already exists.

        Returns:
            `Application`: Application added.
        """
        application = Application.create(
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
        )

        applications = self._repository.find_many(
            name="eq:{}".format(application.name),
            version="eq:{}".format(application.version),
            architect="eq:{}".format(application.architect),
        )

        if applications.total_items:
            raise AlreadyExists(
                "Application with name: {name!r} version: {version!r} and architect: {architect!r} already exists".format(
                    name=application.name,
                    version=application.version,
                    architect=application.architect,
                )
            )

        self._repository.add_one(aggregate=application)
        self._message_bus.publish(domain_events=application.domain_events)
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
            `AlreadyExists`: A Application with the provided email already exists.

        Returns:
            `Application`: Application updated.
        """
        application = self._repository.find_one(id=id)

        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=id)
            )

        application = application.update(
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
        )

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
            raise NotFound(
                "Application with id: {id!r} not found".format(id=id)
            )

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
            raise NotFound(
                "Application with id: {id!r} not found".format(id=id)
            )

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()
