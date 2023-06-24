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
        return (
            "{c}(id={id!r}, name={name!r}, discarded={discarded!r})"
        ).format(
            c=self.__class__.__name__,
            id=self.id,
            name=self.name,
            discarded=self.discarded,
        )

    def to_dict(self, exclude: list[str] | None = None) -> dict:
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
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            discarded=data.get("discarded"),
        )
