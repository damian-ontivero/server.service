"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.server.credential import CredentialDbModel
from st_server.infrastructure.mysql.server.server_application import (
    ServerApplicationDbModel,
)


class ServerDbModel(db.Base):
    """Server database model."""

    __tablename__ = "server"

    id = sa.Column(
        sa.String(32), primary_key=True, unique=True, nullable=False
    )
    name = sa.Column(sa.String(255), nullable=False)
    cpu = sa.Column(sa.String(255), nullable=False)
    ram = sa.Column(sa.String(255), nullable=False)
    hdd = sa.Column(sa.String(255), nullable=False)
    environment_id = sa.Column(sa.ForeignKey("environment.id"), nullable=False)
    operating_system_id = sa.Column(
        sa.ForeignKey("operating_system.id"), nullable=False
    )
    discarded = sa.Column(sa.Boolean, nullable=False, default=False)

    credentials = relationship(CredentialDbModel, lazy="noload")
    applications = relationship(ServerApplicationDbModel, lazy="noload")

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            "{c}(id={id!r}, name={name!r}, cpu={cpu!r}, "
            "ram={ram!r}, hdd={hdd!r}, environment_id={environment_id!r}, "
            "operating_system_id={operating_system_id!r}, "
            "credentials={credentials!r}, "
            "applications={applications!r}, "
            "discarded={discarded!r})"
        ).format(
            c=self.__class__.__name__,
            id=self.id,
            name=self.name,
            cpu=self.cpu,
            ram=self.ram,
            hdd=self.hdd,
            environment_id=self.environment_id,
            operating_system_id=self.operating_system_id,
            credentials=self.credentials,
            applications=self.applications,
            discarded=self.discarded,
        )

    def to_dict(self, exclude: list[str] | None = None) -> dict:
        """Returns a dictionary representation of the object.

        Args:
            exclude (`list[str]`): List of attributes to exclude.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        data = {
            "id": self.id,
            "name": self.name,
            "cpu": self.cpu,
            "ram": self.ram,
            "hdd": self.hdd,
            "environment_id": self.environment_id,
            "operating_system_id": self.operating_system_id,
            "credentials": [
                credential.to_dict() for credential in self.credentials
            ],
            "applications": [
                application.to_dict() for application in self.applications
            ],
            "discarded": self.discarded,
        }

        if exclude:
            for attr in exclude:
                del data[attr]

        return data

    def from_dict(data: dict) -> "ServerDbModel":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `ServerDbModel`: Instance of the class.
        """
        return ServerDbModel(
            id=data.get("id"),
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment_id=data.get("environment_id"),
            operating_system_id=data.get("operating_system_id"),
            credentials=data.get("credentials") or [],
            applications=data.get("applications") or [],
            discarded=data.get("discarded"),
        )
