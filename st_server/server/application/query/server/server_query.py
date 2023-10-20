"""Server query."""

from st_server.server.application.dto.server.server import ServerReadDto
from st_server.server.domain.repository.server.server_repository import (
    ServerRepository,
)
from st_server.shared.application.exception.exception import NotFound
from st_server.shared.application.response.query_response import QueryResponse
from st_server.shared.helper.filter import validate_filter
from st_server.shared.helper.pagination import validate_pagination
from st_server.shared.helper.sort import validate_sort
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class ServerQuery:
    """Server query implementation.

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
        self, repository: ServerRepository, message_bus: MessageBus
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
        limit: int | None = None,
        offset: int | None = None,
        filter: dict | None = None,
        and_filter: list[dict] | None = None,
        or_filter: list[dict] | None = None,
        sort: list[dict] | None = None,
        access_token: str | None = None,
    ) -> QueryResponse:
        """Returns servers."""
        if limit is None:
            limit = 0
        if offset is None:
            offset = 0
        if filter is None:
            filter = {}
        if and_filter is None:
            and_filter = []
        if or_filter is None:
            or_filter = []
        if sort is None:
            sort = []
        servers = self._repository.find_many(
            limit=limit,
            offset=offset,
            filter=filter,
            and_filter=and_filter,
            or_filter=or_filter,
            sort=sort,
        )
        total = servers.total
        return QueryResponse(
            total=total,
            limit=limit,
            offset=offset,
            prev_offset=offset - limit if offset > 0 else None,
            next_offset=offset + limit if offset + limit < total else None,
            items=[
                ServerReadDto.from_entity(server) for server in servers.items
            ],
        )

    # @validate_access_token
    # @validate_permission
    def find_one(
        self, id: str, access_token: str | None = None
    ) -> ServerReadDto:
        """Returns a Server."""
        server = self._repository.find_one(id)
        if server is None:
            raise NotFound("Server with id: {id!r} not found".format(id=id))
        return ServerReadDto.from_entity(server)
