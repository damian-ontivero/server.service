"""Operating system service."""

import math

from st_server.context.server.domain.operating_system.operating_system import (
    OperatingSystem,
)
from st_server.shared.core.exception import AlreadyExists, NotFound
from st_server.shared.core.message_bus import MessageBus
from st_server.shared.core.repository import Repository
from st_server.shared.core.response import ServiceResponse
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort


class OperatingSystemService:
    """Operating system service."""

    def __init__(
        self, repository: Repository, message_bus: MessageBus
    ) -> None:
        """Initializes the service.

        Args:
            repository (`Repository`): Operating system repository.
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
        """Returns all operating systems that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no operating system will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all operating systems will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            per_page (`int` | `None`): Number of records per page. Defaults to `None`.
            page (`int` | `None`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Operating systems found.
        """
        operating_systems = self._repository.find_many(
            fields=fields, limit=per_page, offset=page, sort=sort, **kwargs
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

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> OperatingSystem:
        """Returns the operating system that matches the provided id.

        Args:
            id (`int`): Operating system id.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No operating system found with the provided id.

        Returns:
            `OperatingSystem`: Operating system found.
        """
        operating_system = self._repository.find_one(id=id, fields=fields)

        if operating_system is None:
            raise NotFound(
                "Operating system with id {id!r} not found.".format(id=id)
            )

        return operating_system

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> OperatingSystem:
        """Adds the provided operating system and publishes the OperatingSystem events.

        Args:
            data (`dict`): Dictionary with the operating system data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `AlreadyExists`: An operating system with the provided name already exists.

        Returns:
            `OperatingSystem`: Operating system added.
        """
        operating_system = OperatingSystem.create(**data)
        operating_systems = self._repository.find_many(
            name="eq:{}".format(operating_system.name)
        )

        if operating_systems.total_items:
            raise AlreadyExists(
                "Operating system with name {name!r} already exists.".format(
                    name=operating_system.name
                )
            )

        self._repository.add_one(aggregate=operating_system)
        # self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()

        return self._repository.find_one(id=operating_system.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> OperatingSystem:
        """Updates the operating system that matches the provided id and publishes the events.

        Args:
            id (`str`): Operating system id.
            data (`dict`): Dictionary with the operating system data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No operating system found with the provided id.
            `AlreadyExists`: A operating system with the provided name already exists.

        Returns:
            `OperatingSystem`: Operating system updated.
        """
        operating_system = self._repository.find_one(id=id)

        if operating_system is None:
            raise NotFound(
                "Operating system with id {id!r} not found.".format(id=id)
            )

        for key, value in data.items():
            setattr(operating_system, key, value)

        self._repository.update_one(aggregate=operating_system)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()

        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        """Discards the operating system that matches the provided id and publishes the events.

        Args:
            id (`str`): Operating system id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No operating system found with the provided id.
        """
        operating_system = self._repository.find_one(id=id)

        if operating_system is None:
            raise NotFound(
                "Operating system with id {id!r} not found.".format(id=id)
            )

        operating_system.discard()

        self._repository.update_one(aggregate=operating_system)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        """Deletes the operating system that matches the provided id and publishes the events.

        Args:
            id (`str`): Operating system id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No operating system found with the provided id.
        """
        operating_system = self._repository.find_one(id=id)

        if operating_system is None:
            raise NotFound(
                "Operating system with id {id!r} not found.".format(id=id)
            )

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()
