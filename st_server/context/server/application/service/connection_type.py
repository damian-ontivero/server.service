"""ConnectionType service."""

import math

from st_server.context.server.domain.connection_type.connection_type import (
    ConnectionType,
)
from st_server.shared.core.exception import AlreadyExists, NotFound
from st_server.shared.core.message_bus import MessageBus
from st_server.shared.core.repository import Repository
from st_server.shared.core.response import ServiceResponse
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort


class ConnectionTypeService:
    """ConnectionType service implementation.

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
        connection_types = self._repository.find_many(
            limit=limit, offset=offset, sort=sort, fields=fields, **kwargs
        )
        total = connection_types.total_items
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
            items=connection_types.items,
        )

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> ConnectionType:
        if fields is None:
            fields = []
        connection_type = self._repository.find_one(id=id, fields=fields)
        if connection_type is None:
            raise NotFound(message=f"ConnectionType with id {id} not found.")
        return connection_type

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> ConnectionType:
        connection_type = ConnectionType.create(name=data.get("name"))
        connection_types = self._repository.find_many(
            name="eq:{}".format(connection_type.name)
        )
        if connection_types.total_items:
            raise AlreadyExists(
                "ConnectionType with name: {name!r} already exists".format(
                    name=connection_type.name
                )
            )
        self._repository.add_one(aggregate=connection_type)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()
        return self._repository.find_one(id=connection_type.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> ConnectionType:
        connection_type = self._repository.find_one(id=id)
        if connection_type is None:
            raise NotFound(
                "ConnectionType with id: {id!r} not found".format(id=id)
            )
        connection_type = connection_type.update(name=data.get("name"))
        self._repository.update_one(aggregate=connection_type)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()
        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        connection_type = self._repository.find_one(id=id)
        if connection_type is None:
            raise NotFound(
                "ConnectionType with id: {id!r} not found".format(id=id)
            )
        connection_type.discard()
        self._repository.update_one(aggregate=connection_type)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        connection_type = self._repository.find_one(id=id)
        if connection_type is None:
            raise NotFound(
                "ConnectionType with id: {id!r} not found".format(id=id)
            )
        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=connection_type.domain_events)
        connection_type.clear_domain_events()
