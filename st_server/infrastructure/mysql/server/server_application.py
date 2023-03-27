"""Server Application database model."""

import sqlalchemy as sa

from st_server.infrastructure.mysql import db


class ServerApplicationDbModel(db.Base):
    """Server Application database model."""

    __tablename__ = "server_application"

    server_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("server.id"),
        primary_key=True,
        nullable=False,
    )
    application_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("application.id"),
        primary_key=True,
        nullable=False,
    )
    install_dir = sa.Column(sa.String(255), nullable=True)
    log_dir = sa.Column(sa.String(255), nullable=True)
