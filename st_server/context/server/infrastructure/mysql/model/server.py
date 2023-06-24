"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.context.server.infrastructure.mysql import db


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

    environment = relationship(
        "EnvironmentDbModel", lazy="noload", viewonly=True
    )
    operating_system = relationship(
        "OperatingSystemDbModel", lazy="noload", viewonly=True
    )
    credentials = relationship("CredentialDbModel", lazy="noload")
    applications = relationship("ServerApplicationDbModel", lazy="noload")

    def __repr__(self) -> str:
        return (
            "{c}(id={id!r}, name={name!r}, cpu={cpu!r}, "
            "ram={ram!r}, hdd={hdd!r}, "
            "environment_id={environment_id!r}, "
            "environment={environment!r}, "
            "operating_system_id={operating_system_id!r}, "
            "operating_system={operating_system!r}, "
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
            environment=self.environment,
            operating_system_id=self.operating_system_id,
            operating_system=self.operating_system,
            credentials=self.credentials,
            applications=self.applications,
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
            "environment_id": self.environment_id,
            "environment": self.environment.to_dict()
            if self.environment
            else None,
            "operating_system_id": self.operating_system_id,
            "operating_system": self.operating_system.to_dict()
            if self.operating_system
            else None,
            "credentials": [
                credential.to_dict() for credential in self.credentials
            ],
            "applications": [
                application.to_dict() for application in self.applications
            ],
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
            environment_id=data.get("environment_id"),
            operating_system_id=data.get("operating_system_id"),
            credentials=data.get("credentials") or [],
            applications=data.get("applications") or [],
            discarded=data.get("discarded"),
        )
