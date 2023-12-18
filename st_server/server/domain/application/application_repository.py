from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional

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
    Repository interface for managing Application entities.
    Repositories handle the retrieval and storage of aggregates.

    Methods:
        - find_many: Retrieves a list of Applications based on filtering, sorting, and pagination.
        - find_by_id: Fetches a single Application by its ID.
        - add: Adds a new Application entity to the repository.
        - update: Updates an existing Application entity in the repository.
        - delete_by_id: Deletes an Application entity by its ID.
    """

    @abstractmethod
    def find_many(
        self,
        limit: int,
        offset: int,
        filters: Dict[str, Dict[str, str]],
        and_filters: List[Dict[str, Dict[str, str]]],
        or_filters: List[Dict[str, Dict[str, str]]],
        sort: List[Dict[str, str]],
    ) -> RepositoryResponse:
        """
        Retrieves a list of Applications based on provided filters, sorting, and pagination.

        Args:
            limit (int): Maximum number of records to return.
            offset (int): Number of records to skip.
            filters (Dict[str, Dict[str, str]]): Filter criteria as a dictionary of attribute: operator: value.
            and_filters (List[Dict[str, Dict[str, str]]]): List of 'AND' filter criteria.
            or_filters (List[Dict[str, Dict[str, str]]]): List of 'OR' filter criteria.
            sort (List[Dict[str, str]]): List of sorting criteria.

        Returns:
            RepositoryResponse: Response object containing a list of Application entities.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Application]:
        """
        Retrieves an Application by its ID.

        Args:
            id (int): ID of the Application to retrieve.

        Returns:
            Optional[Application]: The retrieved Application or None if not found.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, application: Application) -> None:
        """
        Adds an Application.

        Args:
            application (Application): The Application entity to add.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, application: Application) -> None:
        """
        Updates an Application.

        Args:
            application (Application): The Application entity to update.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        """
        Deletes an Application by its ID.

        Args:
            id (int): ID of the Application to delete.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError
