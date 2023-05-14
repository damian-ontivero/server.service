"""Environment service."""

import math

from st_server.application.helper.filter import validate_filter
from st_server.application.helper.pagination import validate_pagination
from st_server.application.helper.sort import validate_sort
from st_server.domain.environment.environment import Environment
from st_server.domain.exception import AlreadyExists, NotFound
from st_server.domain.message_bus import MessageBus
from st_server.domain.repository import Repository
from st_server.domain.response import ServiceResponse


class EnvironmentService:
    """Environment service."""

    def __init__(
        self, repository: Repository, message_bus: MessageBus
    ) -> None:
        """Initializes the service.

        Args:
            repository (`Repository`): Environment repository.
            message_bus (`MessageBus`): Message bus.
        """
        self._repository = repository
        self._message_bus = message_bus

    # @AuthService.access_token_required
    @validate_pagination
    @validate_sort
    @validate_filter
    def find_many(
        self,
        fields: list[str] | None = None,
        per_page: int | None = None,
        page: int | None = None,
        sort: list[str] | None = None,
        access_token: str | None = None,
        **kwargs,
    ) -> ServiceResponse:
        """Returns all environments that match the provided conditions.

        If a `None` value is provided to per_page, there will be no pagination.

        If a `Zero` value is provided to per_page, no environment will be returned.

        If a `None` value is provided to page, the first page will be returned.

        If a `None` value is provided to kwargs, all environments will be returned.

        Args:
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            per_page (`int` | `None`): Number of records per page. Defaults to `None`.
            page (`int` | `None`): Page number. Defaults to `None`.
            sort (`list[str]` | `None`): Sort criteria. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Returns:
            `ServiceResponse`: Environments found.
        """
        environments = self._repository.find_many(
            fields=fields, limit=per_page, offset=page, sort=sort, **kwargs
        )
        total = environments.total_items

        return ServiceResponse(
            per_page=per_page,
            page=(page or 1),
            prev_page=((page or 1) - 1) if (page or 1) > 1 else None,
            next_page=((page or 1) + 1)
            if (page or 1) > 0
            and (page or 1)
            < math.ceil(float(total) / float(per_page or total))
            else None,
            last_page=math.ceil(float(total) / float(per_page or total)),
            first_page=1,
            items=environments.items,
        )

    # @AuthService.access_token_required
    def find_one(
        self,
        id: int,
        fields: list[str] | None = None,
        access_token: str | None = None,
    ) -> Environment:
        """Returns the environment that matches the provided id.

        Args:
            id (`int`): Environment id.
            fields (`list[str]` | `None`): List of fields to return. Defaults to `None`.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No environment found with the provided id.

        Returns:
            `Environment`: Environment found.
        """
        environment = self._repository.find_one(id=id, fields=fields)

        if environment is None:
            raise NotFound(message=f"Environment with id {id} not found.")

        return environment

    # @AuthService.access_token_required
    def add_one(
        self, data: dict, access_token: str | None = None
    ) -> Environment:
        """Adds the provided environment and publishes the environment events.

        Args:
            data (`dict`): Dictionary with the environment data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `AlreadyExists`: An environment with the provided name already exists.

        Returns:
            `Environment`: Environment added.
        """
        environment = Environment.create(**data)
        environments = self._repository.find_many(
            name="eq:{}".format(environment.name)
        )

        if environments.total_items:
            raise AlreadyExists(
                message=f"Environment with name {environment.name} already exists."
            )

        self._repository.add_one(aggregate=environment)
        # self._message_bus.publish(domain_events=environment.domain_events)
        environment.clear_domain_events()

        return self._repository.find_one(id=environment.id)

    # @AuthService.access_token_required
    def update_one(
        self, id: str, data: dict, access_token: str | None = None
    ) -> Environment:
        """Updates the environment that matches the provided id and publishes the events.

        Args:
            id (`str`): Environment id.
            data (`dict`): Dictionary with the environment data.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No environment found with the provided id.
            `AlreadyExists`: A environment with the provided name already exists.

        Returns:
            `Environment`: Environment updated.
        """
        environment = self._repository.find_one(id=id)

        if environment is None:
            raise NotFound(message=f"Environment with id {id} not found.")

        for key, value in data.items():
            setattr(environment, key, value)

        self._repository.update_one(aggregate=environment)
        self._message_bus.publish(domain_events=environment.domain_events)
        environment.clear_domain_events()

        return self._repository.find_one(id=id)

    # @AuthService.access_token_required
    def discard_one(self, id: str, access_token: str | None = None) -> None:
        """Discards the environment that matches the provided id and publishes the events.

        Args:
            id (`str`): Environment id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No environment found with the provided id.
        """
        environment = self._repository.find_one(id=id)

        if environment is None:
            raise NotFound(message=f"Environment with id {id} not found.")

        environment.discard()

        self._repository.update_one(aggregate=environment)
        self._message_bus.publish(domain_events=environment.domain_events)
        environment.clear_domain_events()

    # @AuthService.access_token_required
    def delete_one(self, id: str, access_token: str | None = None) -> None:
        """Deletes the environment that matches the provided id and publishes the events.

        Args:
            id (`str`): Environment id.
            access_token (`str` | `None`): Access token. Defaults to `None`.

        Raises:
            `NotFound`: No environment found with the provided id.
        """
        environment = self._repository.find_one(id=id)

        if environment is None:
            raise NotFound(message=f"Environment with id {id} not found.")

        self._repository.delete_one(id=id)
        self._message_bus.publish(domain_events=environment.domain_events)
        environment.clear_domain_events()
