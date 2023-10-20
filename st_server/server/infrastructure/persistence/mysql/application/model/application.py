"""Application database model."""

import sqlalchemy as sa

from st_server.server.domain.entity.application.application import Application
from st_server.server.infrastructure.persistence.mysql import session


class ApplicationDbModel(session.Base):
    """Application database model."""

    __tablename__ = "application"

    id = sa.Column(sa.String(32), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    version = sa.Column(sa.String(255), nullable=False)
    architect = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False)

    @classmethod
    def from_entity(cls, entity: Application) -> "ApplicationDbModel":
        """Named constructor to create a model from an entity."""
        return cls(
            id=entity.id.value,
            name=entity.name,
            version=entity.version,
            architect=entity.architect,
            discarded=entity.discarded,
        )

    def to_dict(self) -> dict:
        """Returns a dictiionary representation of the model."""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "architect": self.architect,
            "discarded": self.discarded,
        }

    def update(self, entity: Application) -> None:
        """Updates the model from an entity."""
        self.name = entity.name
        self.version = entity.version
        self.architect = entity.architect
        self.discarded = entity.discarded
