from st_core.domain.entity_id import EntityId
from st_core.domain.factory import Factory

from st_server.server.domain.application.application import Application


class ApplicationFactory(Factory):
    """Application Factory.

    This Factory is used to build a complete new Application or rebuild an existing Application.
    """

    @staticmethod
    def build(
        name: str,
        version: str,
        architect: str,
    ) -> Application:
        """Static method to create a new Application.

        Important:
            This method is only used to create a new Application.
            When creating a new Application, the id is automatically generated
            and a domain event is registered.
        """
        application = Application(
            id=EntityId.generate(),
            name=name,
            version=version,
            architect=architect,
            discarded=False,
        )
        domain_event = Application.Created(aggregate_id=application._id.value)
        application.register_domain_event(domain_event)
        return application

    @staticmethod
    def rebuild(
        id: str,
        name: str,
        version: str,
        architect: str,
        discarded: bool,
    ) -> Application:
        """Static method to rebuild a Application.

        Important:
            This method is only used to rebuild a Application.
            When rebuilding a Application, the id is not generated
            and a domain event is not registered.
        """
        application = Application(
            id=EntityId.from_text(id),
            name=name,
            version=version,
            architect=architect,
            discarded=discarded,
        )
        return application
