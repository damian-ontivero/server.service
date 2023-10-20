import factory
import factory.fuzzy

from st_server.server.domain.factory.application.application_factory import (
    ApplicationFactory as BaseApplicationFactory,
)
from st_server.server.infrastructure.mysql.application.repositories.application_repository import (
    ApplicationRepositoryImpl,
)
from tests.conftest import SessionLocal


class ApplicationFactory(factory.Factory):
    """Application factory."""

    class Meta:
        model = BaseApplicationFactory

    name = factory.Faker("name")
    version = factory.Faker("name")
    architect = factory.Faker("name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        server = model_class.build(*args, **kwargs)
        ApplicationRepositoryImpl(SessionLocal()).save_one(server)
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.build(*args, **kwargs)
        return server
