import factory
import factory.fuzzy

from st_server.server.domain.server.connection_type import ConnectionType


class ConnectionTypeFactory(factory.Factory):
    class Meta:
        model = ConnectionType

    text = factory.Faker("pystr")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment
