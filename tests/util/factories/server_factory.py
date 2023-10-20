import factory
import factory.fuzzy

from st_server.server.domain.factory.server.server_factory import (
    ServerFactory as BaseServerFactory,
)
from st_server.server.infrastructure.mysql.server.repositories.server_repository import (
    ServerRepositoryImpl,
)
from tests.conftest import SessionLocal
from tests.util.factories.environment import EnvironmentFactory
from tests.util.factories.operating_system import OperatingSystemFactory


class ServerFactory(factory.Factory):
    """Server factory."""

    class Meta:
        model = BaseServerFactory

    name = factory.Faker("name")
    cpu = factory.Faker("pystr")
    ram = factory.Faker("pystr")
    hdd = factory.Faker("pystr")
    environment = factory.SubFactory(EnvironmentFactory)
    operating_system = factory.SubFactory(OperatingSystemFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        server = model_class.build(*args, **kwargs)
        ServerRepositoryImpl(SessionLocal()).save_one(server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.build(*args, **kwargs)
        return server
