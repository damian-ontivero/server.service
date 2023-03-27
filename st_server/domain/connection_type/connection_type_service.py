"""Abstract class defines the Connection Type service interface."""

from abc import abstractmethod

from st_server.domain.connection_type import (
    ConnectionType,
    ConnectionTypeCreate,
    ConnectionTypeUpdate,
)
from st_server.domain.helper import ServiceResponse


class ConnectionTypeAbstractService:
    """Abstract class defines the Connection Type service interface."""

    _session_factory = None

    @classmethod
    @abstractmethod
    def find_many(
        cls,
        per_page: int | None = None,
        page: int | None = None,
        sort: list[str] | None = None,
        access_token: str | None = None,
        **kwargs
    ) -> ServiceResponse:
        """Returns all entities that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no entity will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all entities will be returned.

        Args:
            per_page (`int` | `None`, `optional`): Number of records per page. Defaults to `None`.
            page (`int` | `None`, `optional`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`, `optional`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Entities found.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def find_one(
        cls, id_: int, access_token: str | None = None
    ) -> ConnectionType:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ConnectionTypeNotFound`: No entity found with the provided id.

        Returns:
            `ConnectionType`: Entity found.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def add_one(
        cls, server_dto: ConnectionTypeCreate, access_token: str | None = None
    ) -> ConnectionType:
        """Adds an entity.

        Args:
            server_dto (`ConnectionTypeCreate`): Entity to add.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ConnectionTypeNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `ConnectionType`: Entity added.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update_one(
        cls,
        id_: int,
        server_dto: ConnectionTypeUpdate,
        access_token: str | None = None,
    ) -> ConnectionType:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            server_dto (`ConnectionTypeUpdate`): Entity to update.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ConnectionTypeNotFound`: No entity found with the provided id.
            `ConnectionTypeNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `ConnectionType`: Entity updated.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete_one(
        cls, id_: int, access_token: str | None = None
    ) -> ConnectionType:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ConnectionTypeNotFound`: No entity found with the provided id.

        Returns:
            `ConnectionType`: Entity deleted.
        """
        raise NotImplementedError
