"""Server Repository interface."""

from abc import ABCMeta, abstractmethod

from st_server.server.domain.entities.server import Server
from st_server.shared.domain.repositories.repository_page_dto import (
    RepositoryPageDto,
)

FILTER_OPERATOR_MAPPER = {
    "eq": lambda m, k, v: getattr(m, k) == v,
    "gt": lambda m, k, v: getattr(m, k) > v,
    "ge": lambda m, k, v: getattr(m, k) >= v,
    "lt": lambda m, k, v: getattr(m, k) < v,
    "le": lambda m, k, v: getattr(m, k) <= v,
    "in": lambda m, k, v: getattr(m, k).in_(v.split(",")),
    "btw": lambda m, k, v: getattr(m, k).between(*v.split(",")),
    "lk": lambda m, k, v: getattr(m, k).ilike(f"%{v}%"),
}


class ServerRepository(metaclass=ABCMeta):
    """Server Repository interface.

    Repositories are responsible for retrieving and storing aggregates.

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

    @abstractmethod
    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        **kwargs,
    ) -> RepositoryPageDto:
        """Returns a list of Servers."""
        raise NotImplementedError

    @abstractmethod
    def find_one(
        self,
        id: int,
    ) -> Server | None:
        """Returns a Server."""
        raise NotImplementedError

    @abstractmethod
    def add_one(self, aggregate: Server) -> None:
        """Adds a Server."""
        raise NotImplementedError

    @abstractmethod
    def update_one(self, aggregate: Server) -> None:
        """Updates a Server."""
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id: int) -> None:
        """Deletes a Server."""
        raise NotImplementedError
