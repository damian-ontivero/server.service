"""Application service."""

import math

from st_server.server.application.dtos.application import ApplicationReadDto
from st_server.server.domain.entities.application import Application
from st_server.server.domain.repositories.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.exceptions import AlreadyExists, NotFound
from st_server.shared.application.service_page_dto import ServicePageDto
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class ApplicationService:
    """Application service implementation.

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
        self, repository: ApplicationRepository, message_bus: MessageBus
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
        applications = self._repository.find_many(
            limit=limit, offset=offset, sort=sort, fields=fields, **kwargs
        )
        total = applications._total
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
                ApplicationReadDto.from_entity(application)
                for application in applications._items
            ],
        )

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> Application:
        if fields is None:
            fields = []
        application = self._repository.find_one(id=id, fields=fields)
        if application is None:
            raise NotFound(message=f"Application with id {id} not found.")
        return ApplicationReadDto.from_entity(application)

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> Application:
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
        if applications._total:
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
        return ApplicationReadDto.from_entity(application)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> Application:
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
        return ApplicationReadDto.from_entity(application)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
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
        application = self._repository.find_one(id=id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=id)
            )
        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()
