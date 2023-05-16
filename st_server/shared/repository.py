"""Repository interface."""

from abc import ABCMeta, abstractmethod

from st_server.shared.aggregate_root import AggregateRoot
from st_server.shared.response import RepositoryResponse

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


class Repository(metaclass=ABCMeta):
    """Repository interface."""

    @abstractmethod
    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        fields: list[str] | None = None,
        **kwargs,
    ) -> RepositoryResponse:
        """Returns all aggregates that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no aggregates will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all aggregates will be returned.

        Args:
            limit (`int` | `None`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`): Offset number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.

        Returns:
            `RepositoryResponse`: Aggregates found.
        """
        raise NotImplementedError

    @abstractmethod
    def find_one(
        self, id: int, fields: list[str] | None = None
    ) -> AggregateRoot:
        """Returns the aggregate that matches the provided id.

        If no aggregates match, the value `None` is returned.

        Args:
            id (`int`): Aggregate id.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.

        Returns:
            `AggregateRoot`: Aggregate found.
        """
        raise NotImplementedError

    @abstractmethod
    def add_one(self, aggregate: AggregateRoot) -> None:
        """Adds the provided aggregate.

        Args:
            aggregate (`AggregateRoot`): Aggregate to add.
        """
        raise NotImplementedError

    @abstractmethod
    def update_one(self, aggregate: AggregateRoot) -> None:
        """Updates the provided aggregate.

        Args:
            aggregate (`AggregateRoot`): Aggregate to update.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id: int) -> None:
        """Deletes the aggregate that matches the provided id.

        Args:
            id (`int`): Aggregate id.
        """
        raise NotImplementedError
