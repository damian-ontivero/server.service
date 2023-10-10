"""Server Repository interface."""

from abc import ABCMeta, abstractmethod

from st_server.server.domain.entity.server import Server
from st_server.shared.domain.repository.repository_page_dto import (
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

    In the `find_many` method, the `_filter` parameter is a dictionary that
    contains the _filter criteria. The `_and_filter` and `_or_filter` parameters
    are lists of dictionaries that contain the _filter criteria. The `_sort`
    parameter is a list of dictionaries that contain the _sort criteria.

    The `_filter`, `_and_filter` and `_or_filter` parameters are
    dictionaries with the following structure:

    {
        "attribute": {
            "operator": "value"
        }
    }

    The `attribute` is the name of the attribute to _filter by. The `operator`
    is the operator to _filter by. The `value` is the value to _filter by. The
    following operators are supported:

    - `eq`: equal to
    - `gt`: greater than
    - `ge`: greater than or equal to
    - `lt`: less than
    - `le`: less than or equal to
    - `in`: in
    - `btw`: between
    - `lk`: ilike

    The `in` operator expects a comma-separated list of values. The `btw`
    operator expects a comma-separated list of two values.

    The `_sort` parameter is a list of dictionaries with the following
    structure:

    {
        "attribute": "order"
    }

    The `attribute` is the name of the attribute to _sort by. The `order` is the
    order to _sort by. The following orders are supported:

    - `asc`: ascending
    - `desc`: descending

    The `_limit` parameter is the maximum number of records to return. The
    `_offset` parameter is the number of records to skip.

    The `find_one` method returns a single aggregate. The `id` parameter is the
    ID of the aggregate to return.

    The `save_one` method adds a single aggregate. The `aggregate` parameter is
    the aggregate to add.

    The `save_one` method updates a single aggregate. The `aggregate`
    parameter is the aggregate to update.

    The `delete_one` method deletes a single aggregate. The `id` parameter is
    the ID of the aggregate to delete.
    """

    @abstractmethod
    def find_many(
        self,
        _limit: int,
        _offset: int,
        _filter: dict,
        _and_filter: list[dict],
        _or_filter: list[dict],
        _sort: list[dict],
    ) -> RepositoryPageDto:
        """Returns a list of servers."""
        raise NotImplementedError

    @abstractmethod
    def find_one(self, id: int) -> Server | None:
        """Returns a server."""
        raise NotImplementedError

    @abstractmethod
    def save_one(self, aggregate: Server) -> None:
        """Saves a server."""
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id: int) -> None:
        """Deletes a server."""
        raise NotImplementedError
