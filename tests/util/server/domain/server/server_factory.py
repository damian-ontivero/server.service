import factory
import factory.fuzzy

from st_server.server.domain.server.server import Server
from st_server.server.domain.server.server_status import ServerStatus
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.shared.domain.entity_id import EntityId
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
    class Meta:
        model = Server

    id = EntityId.from_text("1234")
    name = factory.Faker("name")
    cpu = factory.Faker("pystr")
    ram = factory.Faker("pystr")
    hdd = factory.Faker("pystr")
    environment = factory.SubFactory(EnvironmentFactory)
    operating_system = factory.SubFactory(OperatingSystemFactory)
    credentials = factory.List([factory.SubFactory(CredentialFactory)])
    applications = factory.List([factory.SubFactory(ServerApplicationFactory)])
    status = ServerStatus.from_text("stopped")
    discarded = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> Server:
        server = model_class(*args, **kwargs)
        ServerRepositoryImpl(SessionLocal()).add(server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs) -> Server:
        server = model_class(*args, **kwargs)
        return server
