"""Application database model."""

import sqlalchemy as sa

from st_server.server.infrastructure.mysql import db
from st_server.server.domain.entity.application import Application


class ApplicationDbModel(db.Base):
    """Application database model."""

    __tablename__ = "application"

    id = sa.Column(sa.String(32), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    version = sa.Column(sa.String(255), nullable=False)
    architect = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False)

    @classmethod
    def from_entity(cls, entity: Application) -> "ApplicationDbModel":
        """Named constructor to create an Application model from an Application entity."""
        return cls(
            id=entity.id.value,
            name=entity.name,
            version=entity.version,
            architect=entity.architect,
            discarded=entity.discarded,
        )

    def update(self, entity: Application) -> None:
        """Updates the Application model from an Application entity."""
        self.name = entity.name
        self.version = entity.version
        self.architect = entity.architect
        self.discarded = entity.discarded
