"""Connection type service."""

import math

from st_server.application.helper.filter import validate_filter
from st_server.application.helper.pagination import validate_pagination
from st_server.application.helper.sort import validate_sort
from st_server.domain.connection_type.connection_type import ConnectionType
from st_server.domain.exception import AlreadyExists, NotFound
from st_server.domain.message_bus import MessageBus
from st_server.domain.repository import Repository
from st_server.domain.response import ServiceResponse


class ConnectionTypeService:
    """Connection type service."""

    def __init__(
        self, repository: Repository, message_bus: MessageBus
    ) -> None:
        """Initializes the service.

        Args:
            repository (`Repository`): Connection type repository.
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
        """Returns all connection types that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no connection type will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all connection types will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            per_page (`int` | `None`): Number of records per page. Defaults to `None`.
            page (`int` | `None`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Connection types found.
        """
        connection_types = self._repository.find_many(
            fields=fields, limit=per_page, offset=page, sort=sort, **kwargs
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

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> ConnectionType:
        """Returns the connection type that matches the provided id.

        Args:
            id (`int`): connection type id.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No connection type found with the provided id.

        Returns:
            `ConnectionType`: Connection type found.
        """
        connection_type = self._repository.find_one(id=id, fields=fields)

        if connection_type is None:
            raise NotFound(
                "Connection type with id {id!r} not found.".format(id=id)
            )

        return connection_type

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> ConnectionType:
        """Adds the provided connection type and publishes the connection type events.

        Args:
            data (`dict`): Dictionary with the connection type data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `AlreadyExists`: A connection type with the provided name already exists.

        Returns:
            `ConnectionType`: Connection type added.
        """
        connection_type = ConnectionType.create(**data)
        connection_types = self._repository.find_many(
            name="eq:{}".format(connection_type.name)
        )

        if connection_types.total_items:
            raise AlreadyExists(
                "Connection type with name {name!r} already exists.".format(
                    name=connection_type.name
                )
            )

        self._repository.add_one(aggregate=connection_type)
        # self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()

        return self._repository.find_one(id=connection_type.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> ConnectionType:
        """Updates the connection type that matches the provided id and publishes the events.

        Args:
            id (`str`): Connection type id.
            data (`dict`): Dictionary with the connection type data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No connection type found with the provided id.
            `AlreadyExists`: A connection type with the provided name already exists.

        Returns:
            `ConnectionType`: Connection type updated.
        """
        connection_type = self._repository.find_one(id=id)

        if connection_type is None:
            raise NotFound(
                "Connection type with id {id!r} not found.".format(id=id)
            )

        for key, value in data.items():
            setattr(connection_type, key, value)

        self._repository.update_one(aggregate=connection_type)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()

        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        """Discards the connection type that matches the provided id and publishes the events.

        Args:
            id (`str`): Connection type id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No connection type found with the provided id.
        """
        connection_type = self._repository.find_one(id=id)

        if connection_type is None:
            raise NotFound(
                "Connection type with id {id!r} not found.".format(id=id)
            )

        connection_type.discard()

        self._repository.update_one(aggregate=connection_type)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        """Deletes the connection type that matches the provided id and publishes the events.

        Args:
            id (`str`): Connection type id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No connection type found with the provided id.
        """
        connection_type = self._repository.find_one(id=id)

        if connection_type is None:
            raise NotFound(
                "Connection type with id {id!r} not found.".format(id=id)
            )

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()
