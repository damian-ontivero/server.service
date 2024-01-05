import factory
import factory.fuzzy

from st_server.shared.domain.entity_id import EntityId


class EntityIdFactory(factory.Factory):
    """Entity Id value object factory."""

    class Meta:
        model = EntityId

    text = factory.Faker("123456")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        environment = model_class.from_text(*args, **kwargs)
        return environment
