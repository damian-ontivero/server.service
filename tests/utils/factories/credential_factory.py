import factory
import factory.fuzzy

from st_server.server.domain.entities.credential import Credential
from st_server.server.domain.value_objects.connection_type import (
    ConnectionType,
)
from st_server.shared.domain.value_objects.entity_id import EntityId


class CredentialFactory(factory.Factory):
    """Credential factory."""

    class Meta:
        model = Credential

    server_id = EntityId.from_string(value="1234")
    connection_type = factory.fuzzy.FuzzyChoice(
        choices=[
            ConnectionType.from_string(value="SSH"),
            ConnectionType.from_string(value="RDP"),
        ]
    )
    username = factory.Faker("name")
    password = factory.Faker("name")
    local_ip = factory.Faker("ipv4")
    local_port = factory.Faker("pyint")
    public_ip = factory.Faker("ipv4")
    public_port = factory.Faker("pyint")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        credential = model_class.create(*args, **kwargs)
        return credential

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        credential = model_class.create(*args, **kwargs)
        return credential
