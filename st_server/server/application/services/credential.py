"""Credential service."""

import math

from st_server.server.application.dtos.credential import CredentialReadDto
from st_server.server.domain.entities.credential import Credential
from st_server.server.domain.repositories.credential_repository import (
    CredentialRepository,
)
from st_server.server.domain.value_objects.connection_type import (
    ConnectionType,
)
from st_server.shared.application.exceptions import AlreadyExists, NotFound
from st_server.shared.application.service_page_dto import ServicePageDto
from st_server.shared.domain.value_objects.entity_id import EntityId
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class CredentialService:
    """Credential service implementation.

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
        self, repository: CredentialRepository, message_bus: MessageBus
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
    ) -> ServicePageDto:
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
        credentials = self._repository.find_many(
            limit=limit, offset=offset, sort=sort, fields=fields, **kwargs
        )
        total = credentials._total
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
                CredentialReadDto.from_entity(credential)
                for credential in credentials._items
            ],
        )

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> Credential:
        if fields is None:
            fields = []
        credential = self._repository.find_one(id=id, fields=fields)
        if credential is None:
            raise NotFound(message=f"Credential with id {id} not found.")
        return CredentialReadDto.from_entity(credential)

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> Credential:
        credential = Credential.create(
            server_id=EntityId.from_string(value=data.get("server_id")),
            connection_type=ConnectionType.from_string(
                value=data.get("connection_type")
            ),
            username=data.get("username"),
            password=data.get("password"),
            local_ip=data.get("local_ip"),
            local_port=data.get("local_port"),
            public_ip=data.get("public_ip"),
            public_port=data.get("public_port"),
        )
        credentials = self._repository.find_many(
            server_id="eq:{}".format(credential.server_id),
            username="eq:{}".format(credential.username),
        )
        if credentials._total:
            raise AlreadyExists(
                "Credential for server id: {server_id!r} with username: {username!r} already exists".format(
                    server_id=credential.server_id,
                    username=credential.username,
                )
            )
        self._repository.add_one(aggregate=credential)
        return CredentialReadDto.from_entity(credential)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> Credential:
        credential = self._repository.find_one(id=id)
        if credential is None:
            raise NotFound(
                "Credential with id: {id!r} not found".format(id=id)
            )
        credential = credential.update(
            server_id=EntityId.from_string(value=data.get("server_id"))
            if data.get("server_id")
            else credential.server_id,
            connection_type=ConnectionType.from_string(
                value=data.get("connection_type")
            )
            if data.get("connection_type")
            else credential.connection_type,
            username=data.get("username"),
            password=data.get("password"),
            local_ip=data.get("local_ip"),
            local_port=data.get("local_port"),
            public_ip=data.get("public_ip"),
            public_port=data.get("public_port"),
        )
        self._repository.update_one(aggregate=credential)
        return CredentialReadDto.from_entity(credential)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        credential = self._repository.find_one(id=id)
        if credential is None:
            raise NotFound(
                "Credential with id: {id!r} not found".format(id=id)
            )
        credential.discard()
        self._repository.update_one(aggregate=credential)

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        credential = self._repository.find_one(id=id)
        if credential is None:
            raise NotFound(
                "Credential with id: {id!r} not found".format(id=id)
            )
        self._repository.delete_one(id=id)
