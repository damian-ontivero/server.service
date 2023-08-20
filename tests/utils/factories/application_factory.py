import factory
import factory.fuzzy

from st_server.server.domain.entities.application import Application
from st_server.server.infrastructure.mysql.repositories.application_repository import (
    ApplicationRepositoryImpl,
)
from tests.conftest import SessionLocal


class ApplicationFactory(factory.Factory):
    """Application factory."""

    class Meta:
        model = Application

    name = factory.Faker("name")
    version = factory.Faker("name")
    architect = factory.Faker("name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        ApplicationRepositoryImpl(session=SessionLocal()).add_one(
            aggregate=server
        )
        return server

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        server = model_class.create(*args, **kwargs)
        return server
