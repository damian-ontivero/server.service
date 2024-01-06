import factory
import factory.fuzzy

from st_server.server.domain.server.server_application import ServerApplication
from st_server.shared.domain.entity_id import EntityId


class ServerApplicationFactory(factory.Factory):
    class Meta:
        model = ServerApplication

    server_id = EntityId.from_text("123456").value
    application_id = EntityId.from_text("123456").value
    install_dir = factory.Faker("pystr")
    log_dir = factory.Faker("pystr")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        environment = model_class.from_data(*args, kwargs)
        return environment

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        environment = model_class.from_data(*args, kwargs)
        return environment
