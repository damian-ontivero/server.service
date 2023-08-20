"""Credential query parameter."""

from pydantic import BaseModel


class CredentialQueryParameter(BaseModel):
    """Credential query parameter."""

    id: str | None = None
    server_id: str | None = None
    connection_type: str | None = None
    username: str | None = None
    password: str | None = None
    local_ip: str | None = None
    local_port: str | None = None
    public_ip: str | None = None
    public_port: str | None = None
    discarded: bool | None = None
