"""Abstract class defines the Server service interface."""

from abc import abstractmethod

from st_server.domain.helper import ServiceResponse
from st_server.domain.server import Server, ServerCreate, ServerUpdate


class ServerAbstractService:
    """Abstract class defines the Server service interface."""

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
    def find_one(cls, id_: int, access_token: str | None = None) -> Server:
        """Returns the entity that matches the provided id.

        Args:
            id_ (`int`): Entity id.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ServerNotFound`: No entity found with the provided id.

        Returns:
            `Server`: Entity found.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def add_one(
        cls, server_dto: ServerCreate, access_token: str | None = None
    ) -> Server:
        """Adds an entity.

        Args:
            server_dto (`ServerCreate`): Entity to add.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ServerNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `Server`: Entity added.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update_one(
        cls,
        id_: int,
        server_dto: ServerUpdate,
        access_token: str | None = None,
    ) -> Server:
        """Updates an entity.

        Args:
            id_ (`int`): Entity id.
            server_dto (`ServerUpdate`): Entity to update.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ServerNotFound`: No entity found with the provided id.
            `ServerNameAlreadyExists`: An entity with the provided name already exists.

        Returns:
            `Server`: Entity updated.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete_one(cls, id_: int, access_token: str | None = None) -> Server:
        """Deletes an entity.

        Args:
            id_ (`int`): Entity id.
            access_token (`str` | `None`, `optional`): Access token. Defaults to `None`.

        Raises:
            `ServerNotFound`: No entity found with the provided id.

        Returns:
            `Server`: Entity deleted.
        """
        raise NotImplementedError
