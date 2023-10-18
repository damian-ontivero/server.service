import factory
import factory.fuzzy

from st_server.server.domain.server.value_objects.environment import (
    Environment,
)


class EnvironmentFactory(factory.Factory):
    """Environment value object factory."""

    class Meta:
        model = Environment

    text = factory.Faker("pystr")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment.value

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment.value
