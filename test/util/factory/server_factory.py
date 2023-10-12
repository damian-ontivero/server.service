import factory
import factory.fuzzy

from st_server.server.domain.entity.server import Server
from test.util.factory.environment import EnvironmentFactory
from test.util.factory.operating_system import OperatingSystemFactory
from st_server.server.infrastructure.mysql.repository.server_repository import (
    ServerRepositoryImpl,
)
from test.conftest import SessionLocal


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

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        ServerRepositoryImpl(session=SessionLocal()).save_one(aggregate=server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        return server
