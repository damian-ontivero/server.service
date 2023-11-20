import factory
import factory.fuzzy
from st_core.domain.entity_id import EntityId

from st_server.server.domain.server.connection_type import ConnectionType
from st_server.server.domain.server.credential import Credential


class CredentialFactory(factory.Factory):
    """Credential factory."""

    class Meta:
        model = Credential

    server_id = EntityId.from_text("1234")
    connection_type = factory.fuzzy.FuzzyChoice(
        choices=[
            ConnectionType.from_text("SSH"),
            ConnectionType.from_text("RDP"),
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
