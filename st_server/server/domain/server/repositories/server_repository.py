"""Server Repository interface."""

from abc import ABCMeta, abstractmethod

from st_server.server.domain.server.entities.server import Server
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

    In the `find_many` method, the `filter` parameter is a dictionary that
    contains the filter criteria. The `and_filter` and `or_filter` parameters
    are lists of dictionaries that contain the filter criteria. The `sort`
    parameter is a list of dictionaries that contain the sort criteria.

    The `filter`, `and_filter` and `or_filter` parameters are
    dictionaries with the following structure:

    {
        "attribute": {
            "operator": "value"
        }
    }

    The `attribute` is the name of the attribute to filter by. The `operator`
    is the operator to filter by. The `value` is the value to filter by. The
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

    The `sort` parameter is a list of dictionaries with the following
    structure:

    {
        "attribute": "order"
    }

    The `attribute` is the name of the attribute to sort by. The `order` is the
    order to sort by. The following orders are supported:

    - `asc`: ascending
    - `desc`: descending

    The `limit` parameter is the maximum number of records to return. The
    `offset` parameter is the number of records to skip.

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
        limit: int,
        offset: int,
        filter: dict,
        and_filter: list[dict],
        or_filter: list[dict],
        sort: list[dict],
    ) -> RepositoryPageDto:
        """Returns a list of Servers."""
        raise NotImplementedError

    @abstractmethod
    def find_one(self, id: int) -> Server | None:
        """Returns a Server."""
        raise NotImplementedError

    @abstractmethod
    def save_one(self, aggregate: Server) -> None:
        """Saves a Server."""
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id: int) -> None:
        """Deletes a Server."""
        raise NotImplementedError
