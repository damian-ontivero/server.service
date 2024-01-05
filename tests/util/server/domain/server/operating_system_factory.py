import factory
import factory.fuzzy

from st_server.server.domain.server.operating_system import OperatingSystem


class OperatingSystemFactory(factory.Factory):
    """Operating System value object factory."""

    class Meta:
        model = OperatingSystem

    name = factory.Faker("name")
    version = factory.Faker("pystr")
    architecture = factory.Faker("pystr")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        operating_system = model_class.from_data(*args, kwargs)
        return operating_system

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        operating_system = model_class.from_data(*args, kwargs)
        return operating_system
