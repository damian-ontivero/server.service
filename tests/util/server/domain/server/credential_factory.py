import factory
import factory.fuzzy

from st_server.server.server.domain.credential import Credential
from st_server.shared.domain.entity_id import EntityId
from tests.util.server.domain.server.connection_type_factory import (
    ConnectionTypeFactory,
)


class CredentialFactory(factory.Factory):
    class Meta:
        model = Credential

    id = EntityId.from_text("1234")
    server_id = EntityId.from_text("123456")
    connection_type = factory.SubFactory(ConnectionTypeFactory)
    username = factory.Faker("name")
    password = factory.Faker("name")
    local_ip = factory.Faker("ipv4")
    local_port = factory.Faker("pyint")
    public_ip = factory.Faker("ipv4")
    public_port = factory.Faker("pyint")
    discarded = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        credential = model_class(*args, **kwargs)
        return credential

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        credential = model_class(*args, **kwargs)
        return credential
