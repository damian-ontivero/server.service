"""Server database model."""

from datetime import datetime

import pytz
import sqlalchemy as sa

from st_server.infrastructure.mysql import db


class ServerDbModel(db.Base):
    """Server database model."""

    __tablename__ = "server"

    id = sa.Column(
        sa.Integer, autoincrement=True, primary_key=True, nullable=False
    )
    name = sa.Column(sa.String(255), nullable=False)
    environment_id = sa.Column(
        sa.Integer, sa.ForeignKey("environment.id"), nullable=False
    )
    operating_system_id = sa.Column(
        sa.Integer, sa.ForeignKey("operating_system.id"), nullable=False
    )
    cpu = sa.Column(sa.String(255), nullable=False)
    ram = sa.Column(sa.String(255), nullable=False)
    hdd = sa.Column(sa.String(255), nullable=False)
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
