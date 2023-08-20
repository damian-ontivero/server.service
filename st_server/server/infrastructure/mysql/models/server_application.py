"""ServerApplication database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.server.infrastructure.mysql import db


class ServerApplicationDbModel(db.Base):
    """ServerApplication database model."""

    __tablename__ = "server_application"

    server_id = sa.Column(
        sa.ForeignKey("server.id"), primary_key=True, nullable=False
    )
    application_id = sa.Column(
        sa.ForeignKey("application.id"), primary_key=True, nullable=False
    )
    install_dir = sa.Column(sa.String(255), nullable=True)
    log_dir = sa.Column(sa.String(255), nullable=True)

    application = relationship("ApplicationDbModel", lazy="joined")

    def __repr__(self) -> str:
        return (
            "{c}(server_id={server_id!r}, application_id={application_id!r}, "
            "install_dir={install_dir!r}, log_dir={log_dir!r}, "
            "application={application!r})"
        ).format(
            c=self.__class__.__name__,
            server_id=self.server_id,
            application_id=self.application_id,
            install_dir=self.install_dir,
            log_dir=self.log_dir,
            application=self.application,
        )

    def to_dict(self, exclude: list[str] | None = None) -> dict:
        if exclude is None:
            exclude = []
        data = {
            "server_id": self.server_id,
            "application_id": self.application_id,
            "install_dir": self.install_dir,
            "log_dir": self.log_dir,
            "application": self.application.to_dict(),
        }
        return {k: v for k, v in data.items() if k not in exclude}

    @classmethod
    def from_dict(cls, data: dict) -> "ServerApplicationDbModel":
        return cls(
            server_id=data.get("server_id"),
            application_id=data.get("application_id"),
            install_dir=data.get("install_dir"),
            log_dir=data.get("log_dir"),
        )
