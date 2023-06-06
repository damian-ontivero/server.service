"""Server service."""

import math

from st_server.context.server.domain.server.server import Server
from st_server.shared.core.exception import AlreadyExists, NotFound
from st_server.shared.core.message_bus import MessageBus
from st_server.shared.core.repository import Repository
from st_server.shared.core.response import ServiceResponse
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort


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
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        fields: list[str] | None = None,
        access_token: str | None = None,
        **kwargs,
    ) -> ServiceResponse:
        """Returns all Servers that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no Server will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all Servers will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Servers found.
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

        servers = self._repository.find_many(
            limit=limit, offset=offset, sort=sort, fields=fields, **kwargs
        )
        total = servers.total_items

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
        if fields is None:
            fields = []

        server = self._repository.find_one(id=id, fields=fields)

        if server is None:
            raise NotFound(message=f"Server with id {id} not found.")

        return server

    # @AuthService.access_token_required
    def add_one(self, data: dict, access_token: str | None = None) -> Server:
        """Adds the provided Server and publishes the Server events.

        Args:
            data (`dict`): Dictionary with the Server data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `AlreadyExists`: An Server with the provided email already exists.

        Returns:
            `Server`: Server added.
        """
        server = Server.create(
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment_id=data.get("environment_id"),
            operating_system_id=data.get("operating_system_id"),
            credentials=data.get("credentials"),
            applications=data.get("applications"),
        )

        servers = self._repository.find_many(name="eq:{}".format(server.name))

        if servers.total_items:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(
                    name=server.name
                )
            )

        self._repository.add_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
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
            `AlreadyExists`: A Server with the provided email already exists.

        Returns:
            `Server`: Server updated.
        """
        server = self._repository.find_one(id=id)

        if server is None:
            raise NotFound("Server with id: {id!r} not found".format(id=id))

        server = server.update(
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment_id=data.get("environment_id"),
            operating_system_id=data.get("operating_system_id"),
            credentials=data.get("credentials"),
            applications=data.get("applications"),
        )

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
            raise NotFound("Server with id: {id!r} not found".format(id=id))

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
            raise NotFound("Server with id: {id!r} not found".format(id=id))

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
