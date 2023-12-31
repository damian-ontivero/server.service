import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property

from st_server.server.domain.application.application import Application
from st_server.server.infrastructure.persistence.mysql import db
from st_server.shared.domain.entity_id import EntityId
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)


class ApplicationDbModel(db.Base):
    """Application database model."""

    __tablename__ = "application"

    _id = sa.Column("id", EntityIdDbType, primary_key=True)
    _name = sa.Column("name", sa.String(255))
    _version = sa.Column("version", sa.String(255))
    _architect = sa.Column("architect", sa.String(255))
    _discarded = sa.Column("discarded", sa.Boolean)


db.Base.registry.map_imperatively(Application, ApplicationDbModel.__table__)
