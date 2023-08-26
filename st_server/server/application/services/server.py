"""Server service."""

import math

from st_server.server.application.dtos.server import ServerReadDto
from st_server.server.domain.entities.credential import Credential
from st_server.server.domain.entities.server import Server
from st_server.server.domain.repositories.server_repository import (
    ServerRepository,
)
from st_server.server.domain.value_objects.connection_type import (
    ConnectionType,
)
from st_server.server.domain.value_objects.environment import Environment
from st_server.server.domain.value_objects.operating_system import (
    OperatingSystem,
)
from st_server.server.domain.value_objects.server_status import ServerStatus
from st_server.shared.application.exceptions import AlreadyExists, NotFound
from st_server.shared.application.service_page_dto import ServicePageDto
from st_server.shared.domain.value_objects.entity_id import EntityId
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class ServerService:
    """Server service implementation.

    In the `find_many` method, the `kwargs` parameter is a dictionary of filters. The
    key is the field name and the value is a string with the filter operator and
    the value separated by a colon.

    The available filter operators are:
    - `eq`: equal
    - `gt`: greater than
    - `ge`: greater than or equal
    - `lt`: less than
    - `le`: less than or equal
    - `in`: in
    - `btw`: between
    - `lk`: like

        Example: `{"name": "lk:John"}`

    In the `find_many` method, the `sort` parameter is a list of strings with the
    field name and the sort criteria separated by a colon.

    The available sort criteria are:
    - asc: ascending
    - desc: descending

        Example: `["name:asc", "age:desc"]`

    In the `find_many` method, the `fields` parameter is a list of strings with the
    field names to be loaded.

    If a `None` value is provided to limit, there will be no pagination.
    If a `Zero` value is provided to limit, no aggregates will be returned.
    If a `None` value is provided to offset, the first offset will be returned.
    If a `None` value is provided to kwargs, all aggregates will be returned.
    """

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the service."""
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
    ) -> ServicePageDto:
        """Returns Servers."""
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
        total = servers._total
        return ServicePageDto(
            _total=total,
            _limit=limit,
            _offset=(offset or 1),
            _prev_offset=((offset or 1) - 1) if (offset or 1) > 1 else None,
            _next_offset=((offset or 1) + 1)
            if (offset or 1) > 0
            and (offset or 1) < math.ceil(float(total) / float(limit or total))
            else None,
            _items=[
                ServerReadDto.from_entity(server=server)
                for server in servers._items
            ],
        )

    # @AuthService.access_token_required
    def find_one(
        self,
        id: str,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> ServerReadDto:
        """Returns a Server."""
        if fields is None:
            fields = []
        server = self._repository.find_one(id=id, fields=fields)
        if server is None:
            raise NotFound(message=f"Server with id {id} not found.")
        return ServerReadDto.from_entity(server=server)

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> ServerReadDto:
        """Adds a Server."""
        server = Server.create(
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment=Environment.from_text(value=data.get("environment"))
            if data.get("environment")
            else None,
            operating_system=OperatingSystem.from_dict(
                value=data.get("operating_system")
            )
            if data.get("operating_system")
            else None,
            credentials=[
                Credential.from_dict(data=credential)
                for credential in data.get("credentials")
            ],
            applications=data.get("applications"),
        )
        servers = self._repository.find_many(name="eq:{}".format(server.name))
        if servers._total > 0:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(
                    name=server.name
                )
            )
        self._repository.add_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
        return ServerReadDto.from_entity(server=server)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> ServerReadDto:
        """Updates a Server."""
        server = self._repository.find_one(id=id)
        if server is None:
            raise NotFound("Server with id: {id!r} not found".format(id=id))
        server = server.update(
            name=data.get("name"),
            cpu=data.get("cpu", ...),
            ram=data.get("ram", ...),
            hdd=data.get("hdd", ...),
            environment=Environment.from_text(value=data.get("environment"))
            if data.get("environment")
            else None,
            operating_system=OperatingSystem.from_dict(
                value=data.get("operating_system")
            )
            if data.get("operating_system")
            else None,
            credentials=[
                Credential.from_dict(data=credential)
                for credential in data.get("credentials")
            ]
            if data.get("credentials")
            else None,
            applications=data.get("applications"),
            status=ServerStatus.from_text(value=data.get("status"))
            if data.get("status")
            else None,
        )
        self._repository.update_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
        return ServerReadDto.from_entity(server=server)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        """Discards a Server."""
        server = self._repository.find_one(id=id)
        if server is None:
            raise NotFound("Server with id: {id!r} not found".format(id=id))
        server.discard()
        self._repository.update_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        """Deletes a Server."""
        server = self._repository.find_one(id=id)
        if server is None:
            raise NotFound("Server with id: {id!r} not found".format(id=id))
        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
