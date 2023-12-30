import sqlalchemy as sa

from st_server.server.domain.application.application import Application
from st_server.server.infrastructure.persistence.mysql import db
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)


class ApplicationDbModel(db.Base):
    """Application database model."""

    __tablename__ = "application"
    __table_args__ = (sa.PrimaryKeyConstraint("id"),)

    id = sa.Column(EntityIdDbType)
    name = sa.Column(sa.String(255))
    version = sa.Column(sa.String(255))
    architect = sa.Column(sa.String(255))
    discarded = sa.Column(sa.Boolean)


db.Base.registry.map_imperatively(
    Application,
    ApplicationDbModel.__table__,
    properties={
        "_id": ApplicationDbModel.id,
        "_name": ApplicationDbModel.name,
        "_version": ApplicationDbModel.version,
        "_architect": ApplicationDbModel.architect,
        "_discarded": ApplicationDbModel.discarded,
    },
)
