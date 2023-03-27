"""Abstract class defines the Server repository interface."""

import abc

from st_server.domain.helper import RepositoryResponse
from st_server.domain.server import Server


class ServerAbstractRepository:
    """Abstract class defines the Server repository interface."""

    @abc.abstractmethod
    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        **kwargs
    ) -> RepositoryResponse:
        """Returns all entities that match the provided conditions.

        If a `None` value is provided to limit, there will be no pagination.

        If a `Zero` value is provided to limit, no entity will be returned.

        If a `None` value is provided to offset, the first offset will be returned.

        If a `None` value is provided to kwargs, all entities will be returned.

        Args:
            limit (`int` | `None`, `optional`): Number of records per offset. Defaults to `None`.
            offset (`int` | `None`, `optional`): offset number. Defaults to `None`.
            sort (`list[str]` | `None`, `optional`): Sort criteria. Defaults to `None`.

        Returns:
            `RepositoryResponse`: Entities found.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_one(self, id: int) -> Server:
        """Returns the entity that matches the provided id.

        If no entities match, the value `None` is returned.

        Args:
            id (`int`): Entity id.

        Returns:
            `Server`: Entity found.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_one(self, entity: Server) -> Server:
        """Adds an entity.

        Args:
            entity (`Server`): Entity to add.

        Returns:
            `Server`: Entity added.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_one(self, entity: Server) -> Server:
        """Updates an entity.

        Args:
            entity (`Server`): Entity to update.

        Returns:
            `Server`: Entity updated.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_one(self, entity: Server) -> Server:
        """Deletes an entity.

        Args:
            entity (`Server`): Entity to delete.

        Returns:
            `Server`: Entity deleted.
        """
        raise NotImplementedError
