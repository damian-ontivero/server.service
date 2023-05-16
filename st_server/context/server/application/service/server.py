"""Server service."""

import math

from st_server.context.server.application.helper.filter import validate_filter
from st_server.context.server.application.helper.pagination import (
    validate_pagination,
)
from st_server.context.server.application.helper.sort import validate_sort
from st_server.context.server.domain.server.server import Server
from st_server.shared.exception import AlreadyExists, NotFound
from st_server.shared.message_bus import MessageBus
from st_server.shared.repository import Repository
from st_server.shared.response import ServiceResponse


class ServerService:
    """Server service."""

    def __init__(
        self, repository: Repository, message_bus: MessageBus
    ) -> None:
        """Initializes the service.

        Args:
            repository (`Repository`): Server repository.
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
        """Returns all Servers that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no Server will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all Servers will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            per_page (`int` | `None`): Number of records per page. Defaults to `None`.
            page (`int` | `None`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Servers found.
        """
        servers = self._repository.find_many(
            fields=fields, limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = servers.total_items

        print("SERVERS: ", servers.items)

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

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> Server:
        """Returns the Server that matches the provided id.

        Args:
            id (`int`): Server id.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Server found with the provided id.

        Returns:
            `Server`: Server found.
        """
        server = self._repository.find_one(id=id, fields=fields)

        if server is None:
            raise NotFound("Server with id {id!r} not found.".format(id=id))

        return server

    # @AuthService.access_token_required
    def add_one(self, data: dict, access_token: str | None = None) -> Server:
        """Adds the provided Server and publishes the Server events.

        Args:
            data (`dict`): Dictionary with the Server data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `AlreadyExists`: An Server with the provided name already exists.

        Returns:
            `Server`: Server added.
        """
        server = Server.create(**data)
        servers = self._repository.find_many(name="eq:{}".format(server.name))

        if servers.total_items:
            raise AlreadyExists(
                "Server with name {name!r} already exists.".format(
                    name=server.name
                )
            )

        self._repository.add_one(aggregate=server)
        # self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()

        return self._repository.find_one(id=server.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> Server:
        """Updates the Server that matches the provided id and publishes the events.

        Args:
            id (`str`): Server id.
            data (`dict`): Dictionary with the Server data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Server found with the provided id.
            `AlreadyExists`: A Server with the provided name already exists.

        Returns:
            `Server`: Server updated.
        """
        server = self._repository.find_one(id=id)

        if server is None:
            raise NotFound("Server with id {id!r} not found.".format(id=id))

        for key, value in data.items():
            setattr(server, key, value)

        self._repository.update_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()

        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        """Discards the Server that matches the provided id and publishes the events.

        Args:
            id (`str`): Server id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Server found with the provided id.
        """
        server = self._repository.find_one(id=id)

        if server is None:
            raise NotFound("Server with id {id!r} not found.".format(id=id))

        server.discard()

        self._repository.update_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        """Deletes the Server that matches the provided id and publishes the events.

        Args:
            id (`str`): Server id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No Server found with the provided id.
        """
        server = self._repository.find_one(id=id)

        if server is None:
            raise NotFound("Server with id {id!r} not found.".format(id=id))

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
