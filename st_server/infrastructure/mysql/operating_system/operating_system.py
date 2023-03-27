"""Operating System database model."""

from datetime import datetime

import pytz
import sqlalchemy as sa

from st_server.infrastructure.mysql import db


class OperatingSystemDbModel(db.Base):
    """Operating System database model."""

    __tablename__ = "operating_system"

    id = sa.Column(
        sa.Integer, autoincrement=True, primary_key=True, nullable=False
    )
    name = sa.Column(sa.String(255), nullable=False)
    version = sa.Column(sa.String(255), nullable=False)
    architect = sa.Column(sa.String(255), nullable=False)
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
