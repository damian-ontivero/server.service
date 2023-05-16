"""Server Application database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.context.server.infrastructure.mysql import db


class ServerApplicationDbModel(db.Base):
    """Server Application database model."""

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
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
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
        """Returns a dictionary representation of the object.

        Args:
            exclude (`list[str]`): List of attributes to exclude.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        data = {
            "server_id": self.server_id,
            "application_id": self.application_id,
            "install_dir": self.install_dir,
            "log_dir": self.log_dir,
            "application": self.application.to_dict(),
        }

        if exclude:
            for attr in exclude:
                del data[attr]

        return data

    def from_dict(data: dict) -> "ServerApplicationDbModel":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.
        """
        return ServerApplicationDbModel(**data)
