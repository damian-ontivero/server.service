import factory
import factory.fuzzy

from st_server.server.domain.entities.server import Server
from st_server.server.domain.value_objects.environment import Environment
from st_server.server.domain.value_objects.operating_system import (
    OperatingSystem,
)
from st_server.server.infrastructure.mysql.repositories.server_repository import (
    ServerRepositoryImpl,
)
from tests.conftest import SessionLocal


class ServerFactory(factory.Factory):
    """Server factory."""

    class Meta:
        model = Server

    name = factory.Faker("name")
    cpu = factory.Faker("pyint")
    ram = factory.Faker("pyint")
    hdd = factory.Faker("pyint")
    environment = Environment.from_string(value="DEV")
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
        ServerRepositoryImpl(session=SessionLocal()).add_one(aggregate=server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        return server
