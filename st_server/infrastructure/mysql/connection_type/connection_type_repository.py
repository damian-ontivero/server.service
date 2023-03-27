"""Connection Type repository."""

import abc

from sqlalchemy.orm import Session

from st_server.domain.connection_type import ConnectionType
from st_server.domain.helper import RepositoryResponse
from st_server.infrastructure.mysql import db


class ConnectionTypeRepository:
    """Connection Type repository."""

    def __init__(self, session: Session, model: db.Base) -> None:
        """Connection Type repository.

        Args:
            session (`Session`): SQLAlchemy session object.
            model (`db.Base`): SQLAlchemy mapper model.
        """
        self._session = session
        self._model = model
        self._filter_operator_mapper = {
            "eq": lambda k, v: getattr(self._model, k) == v,
            "gt": lambda k, v: getattr(self._model, k) > v,
            "ge": lambda k, v: getattr(self._model, k) >= v,
            "lt": lambda k, v: getattr(self._model, k) < v,
            "le": lambda k, v: getattr(self._model, k) <= v,
            "in": lambda k, v: getattr(self._model, k).in_(v.split(",")),
            "btw": lambda k, v: getattr(self._model, k).between(*v.split(",")),
            "lk": lambda k, v: getattr(self._model, k).ilike(f"%{v}%"),
        }

    @abc.abstractmethod
    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        sort: list[str] | None = None,
        **kwargs,
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
        with self._session as session:
            query = session.query(self._model)

            for attr, value in kwargs.items():
                if hasattr(self._model, attr):
                    op, val = value.split(":")
                    query = query.filter(
                        self._filter_operator_mapper[op](attr, val)
                    )

            if sort:
                for sort_criteria in sort:
                    attr, direction = sort_criteria.split(":")

                    if hasattr(self._model, attr):
                        sorting = getattr(
                            getattr(self._model, attr), direction
                        )
                        query = query.order_by(sorting())

            total = query.count()
            query = query.limit(limit or total)
            query = query.offset(((offset or 1) - 1) * (limit or total))

            return RepositoryResponse(total_items=total, items=query.all())

    @abc.abstractmethod
    def find_one(self, id: int) -> ConnectionType:
        """Returns the entity that matches the provided id.

        If no entities match, the value `None` is returned.

        Args:
            id (`int`): Entity id.

        Returns:
            `ConnectionType`: Entity found.
        """
        with self._session as session:
            return session.query(self._model).get(ident=id)

    @abc.abstractmethod
    def add_one(self, entity: ConnectionType) -> ConnectionType:
        """Adds an entity.

        Args:
            entity (`ConnectionType`): Entity to add.

        Returns:
            `ConnectionType`: Entity added.
        """
        with self._session as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

            return entity

    @abc.abstractmethod
    def update_one(self, entity: ConnectionType) -> ConnectionType:
        """Updates an entity.

        Args:
            entity (`ConnectionType`): Entity to update.

        Returns:
            `ConnectionType`: Entity updated.
        """
        with self._session as session:
            entity = session.merge(entity)
            session.commit()
            session.refresh(entity)

            return entity

    @abc.abstractmethod
    def delete_one(self, entity: ConnectionType) -> ConnectionType:
        """Deletes an entity.

        Args:
            entity (`ConnectionType`): Entity to delete.

        Returns:
            `ConnectionType`: Entity deleted.
        """
        with self._session as session:
            session.delete(entity)
            session.commit()

            return entity
