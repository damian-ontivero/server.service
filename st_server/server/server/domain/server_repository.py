from abc import ABCMeta, abstractmethod

from st_server.server.server.domain.server import Server
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


class ServerRepository(metaclass=ABCMeta):
    """
    Interface for Server repositories.
    This interface should be implemented by any repository
    that is going to be used to retrieve and persist Server
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
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> Server | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, server: Server) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, server: Server) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        raise NotImplementedError
