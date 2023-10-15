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

    def update(self, data: dict) -> None:
        """Updates the application model from a dictionary."""
        self.name = data.get("name")
        self.version = data.get("version")
        self.architect = data.get("architect")
        self.discarded = data.get("discarded")
