"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.models.credential import (
    CredentialDbModel,
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
    discarded = sa.Column(sa.Boolean, nullable=False, default=False)

    credentials = relationship(
        "CredentialDbModel", lazy="joined", cascade="all, delete-orphan"
    )
    applications = relationship("ServerApplicationDbModel", lazy="joined")

    def __repr__(self) -> str:
        return (
            "{c}(id={id!r}, name={name!r}, cpu={cpu!r}, "
            "ram={ram!r}, hdd={hdd!r}, "
            "environment={environment!r}, "
            "operating_system={operating_system!r}, "
            "credentials={credentials!r}, "
            "applications={applications!r}, "
            "status={status!r}, "
            "discarded={discarded!r})"
        ).format(
            c=self.__class__.__name__,
            id=self.id,
            name=self.name,
            cpu=self.cpu,
            ram=self.ram,
            hdd=self.hdd,
            environment=self.environment,
            operating_system=self.operating_system,
            credentials=self.credentials,
            applications=self.applications,
            status=self.status,
            discarded=self.discarded,
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
