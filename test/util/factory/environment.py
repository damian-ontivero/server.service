import factory
import factory.fuzzy

from st_server.server.domain.value_object.environment import Environment


class EnvironmentFactory(factory.Factory):
    """Environment value object factory."""

    class Meta:
        model = Environment

    value = factory.Faker("pystr")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment
