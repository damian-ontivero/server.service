import factory
import factory.fuzzy

from st_server.server.domain.entity.server import Server
from st_server.server.domain.value_object.environment import Environment
from st_server.server.domain.value_object.operating_system import (
    OperatingSystem,
)
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
    environment = Environment.from_text(value="DEV")
    operating_system = OperatingSystem.from_dict(
        value={
            "name": "Ubuntu",
            "version": "20.04",
            "architecture": "x86_64",
        }
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        ServerRepositoryImpl(session=SessionLocal()).save_one(aggregate=server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        return server
