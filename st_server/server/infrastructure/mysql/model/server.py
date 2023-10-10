"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.model.credential import (
    CredentialDbModel,
)
from st_server.server.infrastructure.mysql.model.server_application import (
    ServerApplicationDbModel,
)


class ServerDbModel(db.Base):
    """Server database model."""

    __tablename__ = "server"

    id = sa.Column(sa.String(32), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    cpu = sa.Column(sa.String(255), nullable=True)
    ram = sa.Column(sa.String(255), nullable=True)
    hdd = sa.Column(sa.String(255), nullable=True)
    environment = sa.Column(sa.String(255), nullable=False)
    operating_system = sa.Column(sa.JSON, nullable=False)
    status = sa.Column(sa.String(255), nullable=True)
    discarded = sa.Column(sa.Boolean, nullable=False)

    credentials = relationship(
        "CredentialDbModel", lazy="joined", cascade="all, delete-orphan"
    )
    applications = relationship("ServerApplicationDbModel", lazy="joined")

    @classmethod
    def from_dict(cls, data: dict) -> "ServerDbModel":
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment=data.get("environment"),
            operating_system=data.get("operating_system"),
            credentials=[
                CredentialDbModel.from_dict(data=credential)
                for credential in data.get("credentials")
            ],
            applications=data.get("applications") or [],
            status=data.get("status"),
            discarded=data.get("discarded"),
        )

    def to_dict(self, exclude: list[str] | None = None) -> dict:
        if exclude is None:
            exclude = []
        data = {
            "id": self.id,
            "name": self.name,
            "cpu": self.cpu,
            "ram": self.ram,
            "hdd": self.hdd,
            "environment": self.environment,
            "operating_system": self.operating_system
            if self.operating_system
            else None,
            "credentials": [
                credential.to_dict() for credential in self.credentials
            ],
            "applications": [
                application.to_dict() for application in self.applications
            ],
            "status": self.status,
            "discarded": self.discarded,
        }
        return {k: v for k, v in data.items() if k not in exclude}

    def update(self, data: dict) -> None:
        """Updates the server model from a dictionary."""
        self.name = data.get("name")
        self.cpu = data.get("cpu")
        self.ram = data.get("ram")
        self.hdd = data.get("hdd")
        self.environment = data.get("environment")
        self.operating_system = data.get("operating_system")
        self.status = data.get("status")
        self.discarded = data.get("discarded")
        self.credentials = [
            CredentialDbModel.from_dict(data=credential)
            for credential in data.get("credentials")
        ]
        self.applications = [
            ServerApplicationDbModel.from_dict(data=application)
            for application in data.get("applications")
        ]
