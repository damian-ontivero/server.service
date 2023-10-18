"""ServerApplication database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.server.infrastructure.mysql import db


class ServerApplicationDbModel(db.Base):
    """ServerApplication database model."""

    __tablename__ = "server_application"

    server_id = sa.Column(sa.ForeignKey("server.id"), primary_key=True)
    application_id = sa.Column(
        sa.ForeignKey("application.id"), primary_key=True
    )
    install_dir = sa.Column(sa.String(255), nullable=True)
    log_dir = sa.Column(sa.String(255), nullable=True)

    application = relationship("ApplicationDbModel", lazy="subquery")

    def to_dict(self) -> dict:
        """Returns a dictiionary representation of the model."""
        return {
            "server_id": self.server_id,
            "application_id": self.application_id,
            "install_dir": self.install_dir,
            "log_dir": self.log_dir,
        }
