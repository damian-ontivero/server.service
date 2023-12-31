"""ServerApplication database model."""

import sqlalchemy as sa

from st_server.server.domain.server.server_application import ServerApplication
from st_server.server.infrastructure.persistence.mysql import db
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)


class ServerApplicationDbModel(db.Base):
    """ServerApplication database model."""

    __tablename__ = "server_application"

    server_id = sa.Column(
        EntityIdDbType, sa.ForeignKey("server.id"), primary_key=True
    )
    application_id = sa.Column(
        EntityIdDbType, sa.ForeignKey("application.id"), primary_key=True
    )
    install_dir = sa.Column(sa.String(255))
    log_dir = sa.Column(sa.String(255))


db.Base.registry.map_imperatively(
    ServerApplication,
    ServerApplicationDbModel.__table__,
    properties={
        "_server_id": ServerApplicationDbModel.server_id,
        "_application_id": ServerApplicationDbModel.application_id,
        "_install_dir": ServerApplicationDbModel.install_dir,
        "_log_dir": ServerApplicationDbModel.log_dir,
    },
)
