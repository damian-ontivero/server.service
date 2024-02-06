import factory
import factory.fuzzy

from st_server.server.application.domain.application import Application
from st_server.server.application.infrastructure.persistence.mysql.application_repository import (
    ApplicationRepositoryImpl,
)
from tests.conftest import SessionLocal


class ApplicationFactory(factory.Factory):
    class Meta:
        model = Application

    name = factory.Faker("name")
    version = factory.Faker("name")
    architect = factory.Faker("name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        application = model_class.register(*args, **kwargs)
        ApplicationRepositoryImpl(SessionLocal()).add(application)
        return application

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        application = model_class.register(*args, **kwargs)
        return application
