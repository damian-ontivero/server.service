"""Application query."""

from st_server.server.application.dto.application import ApplicationReadDto
from st_server.server.domain.repository.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.exception.exception import (
    NotFound,
)
from st_server.shared.application.response.query_response import QueryResponse
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class ApplicationQuery:
    """Application query implementation.

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

    If a `None` value is provided to limit, there will be no pagination.
    If a `Zero` value is provided to limit, no aggregates will be returned.
    If a `None` value is provided to offset, the first offset will be returned.
    If a `None` value is provided to kwargs, all aggregates will be returned.
    """

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the service."""
        self._repository = repository
        self._message_bus = message_bus

    # @validate_access_token
    # @validate_permission
    @validate_pagination
    @validate_sort
    @validate_filter
    def find_many(
        self,
        _limit: int | None = None,
        _offset: int | None = None,
        _filter: dict | None = None,
        _and_filter: list[dict] | None = None,
        _or_filter: list[dict] | None = None,
        _sort: list[dict] | None = None,
        access_token: str | None = None,
    ) -> QueryResponse:
        """Returns applications."""
        if _limit is None:
            _limit = 0
        if _offset is None:
            _offset = 0
        if _filter is None:
            _filter = {}
        if _and_filter is None:
            _and_filter = []
        if _or_filter is None:
            _or_filter = []
        if _sort is None:
            _sort = []
        applications = self._repository.find_many(
            _limit=_limit,
            _offset=_offset,
            _filter=_filter,
            _and_filter=_and_filter,
            _or_filter=_or_filter,
            _sort=_sort,
        )
        total = applications._total
        return QueryResponse(
            _total=total,
            _limit=_limit,
            _offset=_offset,
            _prev_offset=_offset - _limit if _offset > 0 else None,
            _next_offset=_offset + _limit
            if _offset + _limit < total
            else None,
            _items=[
                ApplicationReadDto.from_entity(application=application)
                for application in applications._items
            ],
        )

    # @validate_access_token
    # @validate_permission
    def find_one(
        self, id: str, access_token: str | None = None
    ) -> ApplicationReadDto:
        """Returns an application."""
        application = self._repository.find_one(id=id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=id)
            )
        return ApplicationReadDto.from_entity(application=application)
