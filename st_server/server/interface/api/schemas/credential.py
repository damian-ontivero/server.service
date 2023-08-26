"""Credential schema."""

from pydantic import BaseModel


class CredentialBase(BaseModel):
    server_id: str | None = None
    connection_type: str | None = None
    username: str | None = None
    password: str | None = None
    local_ip: str | None = None
    local_port: str | None = None
    public_ip: str | None = None
    public_port: str | None = None


class CredentialRead(CredentialBase):
    id: str | None = None
    discarded: bool | None = None


class CredentialUpdate(CredentialBase):
    pass


class CredentialCreate(CredentialBase):
    pass
