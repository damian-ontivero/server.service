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
    environment = sa.Column(sa.String(255), nullable=False)
    operating_system = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False, default=False)

    credentials = relationship(CredentialDbModel, lazy="noload")
    applications = relationship(ServerApplicationDbModel, lazy="noload")

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            f"ServerDbModel(id={self.id}, name={self.name}, "
            f"cpu={self.cpu}, ram={self.ram}, hdd={self.hdd}, "
            f"environment={self.environment}, "
            f"operating_system={self.operating_system}, "
            f"credentials={self.credentials}, applications={self.applications}, "
            f"discarded={self.discarded})"
        )

    def to_dict(self, exclude: list[str] = None) -> dict:
        """Returns a dictionary representation of the object.

        Args:
            exclude (`list[str]`, optional): List of attributes to exclude.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        data = {
            "id": self.id,
            "name": self.name,
            "cpu": self.cpu,
            "ram": self.ram,
            "hdd": self.hdd,
            "environment": self.environment,
            "operating_system": self.operating_system,
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
            environment=data.get("environment"),
            operating_system=data.get("operating_system"),
            credentials=data.get("credentials", []) or [],
            applications=data.get("applications", []) or [],
            discarded=data.get("discarded"),
        )
