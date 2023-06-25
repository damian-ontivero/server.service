"""OperatingSystem service."""

import math

from st_server.context.server.domain.entity.operating_system import (
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
    """OperatingSystem service implementation.

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
        self, repository: Repository, message_bus: MessageBus
    ) -> None:
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
        operating_systems = self._repository.find_many(
            limit=limit, offset=offset, sort=sort, fields=fields, **kwargs
        )
        total = operating_systems.total_items
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
            items=operating_systems.items,
        )

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> OperatingSystem:
        if fields is None:
            fields = []
        operating_system = self._repository.find_one(id=id, fields=fields)
        if operating_system is None:
            raise NotFound(message=f"OperatingSystem with id {id} not found.")
        return operating_system

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> OperatingSystem:
        operating_system = OperatingSystem.create(
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
        )
        operating_systems = self._repository.find_many(
            name="eq:{}".format(operating_system.name),
            version="eq:{}".format(operating_system.version),
            architect="eq:{}".format(operating_system.architect),
        )
        if operating_systems.total_items:
            raise AlreadyExists(
                "OperatingSystem with name: {name!r} version: {version!r} and architect: {architect!r} already exists".format(
                    name=operating_system.name,
                    version=operating_system.version,
                    architect=operating_system.architect,
                )
            )
        self._repository.add_one(aggregate=operating_system)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()
        return self._repository.find_one(id=operating_system.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> OperatingSystem:
        operating_system = self._repository.find_one(id=id)
        if operating_system is None:
            raise NotFound(
                "OperatingSystem with id: {id!r} not found".format(id=id)
            )
        operating_system = operating_system.update(
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
        )
        self._repository.update_one(aggregate=operating_system)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()
        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        operating_system = self._repository.find_one(id=id)
        if operating_system is None:
            raise NotFound(
                "OperatingSystem with id: {id!r} not found".format(id=id)
            )
        operating_system.discard()
        self._repository.update_one(aggregate=operating_system)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        operating_system = self._repository.find_one(id=id)
        if operating_system is None:
            raise NotFound(
                "OperatingSystem with id: {id!r} not found".format(id=id)
            )
        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=operating_system.domain_events)
        operating_system.clear_domain_events()
