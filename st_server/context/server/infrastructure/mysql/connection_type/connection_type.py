"""ConnectionType database model."""

import sqlalchemy as sa

from st_server.context.server.infrastructure.mysql import db


class ConnectionTypeDbModel(db.Base):
    """ConnectionType database model."""

    __tablename__ = "connection_type"

    id = sa.Column(
        sa.String(32), primary_key=True, unique=True, nullable=False
    )
    name = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            "{c}(id={id!r}, name={name!r}, discarded={discarded!r})"
        ).format(
            c=self.__class__.__name__,
            id=self.id,
            name=self.name,
            discarded=self.discarded,
        )

    def to_dict(self, exclude: list[str] | None = None) -> dict:
        """Returns a dictionary representation of the object.

        Args:
            exclude (`list[str]`): List of attributes to exclude.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        if exclude is None:
            exclude = []

        data = {
            "id": self.id,
            "name": self.name,
            "discarded": self.discarded,
        }

        return {k: v for k, v in data.items() if k not in exclude}

    @classmethod
    def from_dict(cls, data: dict) -> "ConnectionTypeDbModel":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `ConnectionTypeDbModel`: Instance of the class.
        """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            discarded=data.get("discarded"),
        )
