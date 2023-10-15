import factory
import factory.fuzzy


from st_server.server.domain.value_object.operating_system import (
    OperatingSystem,
)


class OperatingSystemFactory(factory.Factory):
    """Operating System value object factory."""

    class Meta:
        model = OperatingSystem

    value = {
        "name": "Ubuntu",
        "version": "20.04",
        "architecture": "x86_64",
    }

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        operating_system = model_class.from_data(*args, **kwargs)
        return operating_system

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        operating_system = model_class.from_data(*args, **kwargs)
        return operating_system
