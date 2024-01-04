from abc import ABCMeta, abstractmethod

from st_server.server.domain.application.application import Application
from st_server.shared.domain.repository_response import RepositoryResponse

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


class ApplicationRepository(metaclass=ABCMeta):
    """
    Interface for Application repositories.
    This interface should be implemented by any repository
    that is going to be used to retrieve and persist Application
    instances.
    """

    @abstractmethod
    def find_many(
        self,
        limit: int,
        offset: int,
        filters: dict[str, dict[str, str]],
        and_filters: list[dict[str, dict[str, str]]],
        or_filters: list[dict[str, dict[str, str]]],
        sort: list[dict[str, str]],
    ) -> RepositoryResponse:
        """Retrieves Applications based on provided filters, sorting, and pagination."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> Application | None:
        """Retrieves an Application by its ID."""
        raise NotImplementedError

    @abstractmethod
    def add(self, application: Application) -> None:
        """Adds an Application."""
        raise NotImplementedError

    @abstractmethod
    def update(self, application: Application) -> None:
        """Updates an Application."""
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        """Deletes an Application by its ID."""
        raise NotImplementedError
