"""Credential database model."""

import sqlalchemy as sa

from st_server.server.infrastructure.mysql import db


class CredentialDbModel(db.Base):
    """Credential database model."""

    __tablename__ = "credential"

    id = sa.Column(sa.String(32), primary_key=True)
    server_id = sa.Column(sa.ForeignKey("server.id"), nullable=False)
    connection_type = sa.Column(sa.String(255), nullable=False)
    local_ip = sa.Column(sa.String(255), nullable=True)
    local_port = sa.Column(sa.String(255), nullable=True)
    public_ip = sa.Column(sa.String(255), nullable=True)
    public_port = sa.Column(sa.String(255), nullable=True)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False)

    @classmethod
    def from_dict(cls, data: dict) -> "CredentialDbModel":
        return cls(
            id=data.get("id"),
            server_id=data.get("server_id"),
            connection_type=data.get("connection_type"),
            local_ip=data.get("local_ip"),
            local_port=data.get("local_port"),
            public_ip=data.get("public_ip"),
            public_port=data.get("public_port"),
            username=data.get("username"),
            password=data.get("password"),
            discarded=data.get("discarded"),
        )

    def to_dict(self, exclude: list[str] | None = None) -> dict:
        if exclude is None:
            exclude = []
        data = {
            "id": self.id,
            "server_id": self.server_id,
            "connection_type": self.connection_type,
            "local_ip": self.local_ip,
            "local_port": self.local_port,
            "public_ip": self.public_ip,
            "public_port": self.public_port,
            "username": self.username,
            "password": self.password,
            "discarded": self.discarded,
        }
        return {k: v for k, v in data.items() if k not in exclude}
