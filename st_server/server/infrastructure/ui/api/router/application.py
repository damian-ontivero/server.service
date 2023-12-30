"""Application router."""

import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from st_server.server.application.application.command.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.command.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from st_server.server.application.application.command.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.application.command.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)
from st_server.server.application.application.command.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.application.command.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_application_query_handler import (
    FindManyApplicationQueryHandler,
)
from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.server.infrastructure.persistence.mysql.application.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.server.infrastructure.ui.api.dependency import (
    get_command_bus,
    get_mysql_session,
    get_rabbitmq_message_bus,
)
from st_server.shared.application.bus.command_bus import CommandBus
from st_server.shared.application.query_response import QueryResponse
from st_server.shared.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)

router = APIRouter(prefix="/server/applications", tags=["Application"])
auth_scheme = HTTPBearer()


def get_repository(session: Session = Depends(get_mysql_session)):
    """Yields a Server repository."""
    return ApplicationRepositoryImpl(session)


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str = Query(default="[]"),
    or_filter: str = Query(default="[]"),
    sort: str = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
):
    """Route to get all applications."""
    query = FindManyApplicationQuery(
        limit=limit,
        offset=offset,
        filter=json.loads(filter),
        and_filter=json.loads(and_filter),
        or_filter=json.loads(or_filter),
        sort=json.loads(sort),
    )
    handler = FindManyApplicationQueryHandler(repository)
    applications = handler.handle(query)
    if applications.total == 0:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=applications.to_dict()),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ApplicationDto)
def get(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
):
    """Route to get an Application by id."""
    query = FindOneApplicationQuery(id=id)
    handler = FindOneApplicationQueryHandler(repository)
    application = handler.handle(query)
    return JSONResponse(
        content=jsonable_encoder(obj=application),
        status_code=status.HTTP_200_OK,
    )


@router.post("", response_model=ApplicationDto)
def create(
    command: AddApplicationCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
):
    """Route to create an Application."""
    command_bus.register(
        command=AddApplicationCommand,
        handler=AddApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ),
    )
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ApplicationDto)
def update(
    id: str,
    command: UpdateApplicationCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
):
    """Route to update an Application."""
    command.id = id
    command_bus.register(
        command=UpdateApplicationCommand,
        handler=UpdateApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ),
    )
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_200_OK,
    )


@router.delete("/{id}")
def delete(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
):
    """Route to delete an Application."""
    command = DeleteApplicationCommand(id=id)
    command_bus.register(
        command=DeleteApplicationCommand,
        handler=DeleteApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ),
    )
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Application has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
