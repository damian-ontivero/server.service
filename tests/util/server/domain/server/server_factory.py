import factory
import factory.fuzzy

from st_server.server.domain.server.server import Server
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from tests.conftest import SessionLocal
from tests.util.server.domain.server.credential_factory import (
    CredentialFactory,
)
from tests.util.server.domain.server.environment_factory import (
    EnvironmentFactory,
)
from tests.util.server.domain.server.operating_system_factory import (
    OperatingSystemFactory,
)
from tests.util.server.domain.server.server_application_factory import (
    ServerApplicationFactory,
)


class ServerFactory(factory.Factory):
    """Server factory."""

    class Meta:
        model = Server

    name = factory.Faker("name")
    cpu = factory.Faker("pystr")
    ram = factory.Faker("pystr")
    hdd = factory.Faker("pystr")
    environment = factory.SubFactory(EnvironmentFactory)
    operating_system = factory.SubFactory(OperatingSystemFactory)
    credentials = factory.List([factory.SubFactory(CredentialFactory)])
    applications = factory.List([factory.SubFactory(ServerApplicationFactory)])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        server = model_class.register(*args, **kwargs)
        ServerRepositoryImpl(SessionLocal()).add(server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.register(*args, **kwargs)
        return server
