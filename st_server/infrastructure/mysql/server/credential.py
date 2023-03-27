"""Credential database model."""

from datetime import datetime

import pytz
import sqlalchemy as sa

from st_server.infrastructure.mysql import db


class CredentialDbModel(db.Base):
    """Credential database model."""

    __tablename__ = "credential"

    id = sa.Column(
        sa.Integer, autoincrement=True, primary_key=True, nullable=False
    )
    server_id = sa.Column(
        sa.Integer, sa.ForeignKey("server.id"), nullable=False
    )
    connection_type_id = sa.Column(
        sa.Integer, sa.ForeignKey("connection_type.id"), nullable=False
    )
    local_ip = sa.Column(sa.String(255), nullable=True)
    local_port = sa.Column(sa.String(255), nullable=True)
    public_ip = sa.Column(sa.String(255), nullable=True)
    public_port = sa.Column(sa.String(255), nullable=True)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=lambda: datetime.now(pytz.timezone("Europe/Madrid")),
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=True,
        onupdate=lambda: datetime.now(pytz.timezone("Europe/Madrid")),
    )
