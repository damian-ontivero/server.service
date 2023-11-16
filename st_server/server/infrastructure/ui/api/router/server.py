"""Server router."""

import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.command_bus.command_bus import CommandBus
from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.command.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.server.command.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.server.command.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.command.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.server.application.server.dto.server import ServerDto
from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.application.server.query.find_many_server_query_handler import (
    FindManyServerQueryHandler,
)
from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.application.server.query.find_one_server_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.persistence.mysql.db import SessionLocal
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
)
from st_server.server.infrastructure.ui.api.dependency import (
    get_command_bus,
    get_mysql_session,
    get_rabbitmq_message_bus,
)
from st_server.shared.application.query_response import QueryResponse

router = APIRouter(prefix="/server/servers", tags=["Server"])
auth_scheme = HTTPBearer()


def get_mysql_repository(session: SessionLocal = Depends(get_mysql_session)):
    """Yields a Server repository."""
    return ServerRepositoryImpl(session)


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str = Query(default="[]"),
    or_filter: str = Query(default="[]"),
    sort: str = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
):
    """Route to get all servers."""
    query = FindManyServerQuery(
        limit=limit,
        offset=offset,
        filter=json.loads(filter),
        and_filter=json.loads(and_filter),
        or_filter=json.loads(or_filter),
        sort=json.loads(sort),
    )
    handler = FindManyServerQueryHandler(repository=repository)
    servers = handler.handle(query)
    if servers.total == 0:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=servers.to_dict()),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ServerDto)
def get(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
):
    """Route to get a Server by id."""
    query = FindOneServerQuery(id=id)
    handler = FindOneServerQueryHandler(repository=repository)
    server = handler.handle(query)
    return JSONResponse(
        content=jsonable_encoder(obj=server), status_code=status.HTTP_200_OK
    )


@router.post("", response_model=ServerDto)
def create(
    command: AddServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
):
    """Route to create a Server."""
    command_bus.register(
        command=AddServerCommand,
        handler=AddServerCommandHandler(
            repository=repository, message_bus=message_bus
        ),
    )
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ServerDto)
def update(
    id: str,
    command: UpdateServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
):
    """Route to update a Server."""
    command.id = id
    command_bus.register(
        command=command,
        handler=UpdateServerCommandHandler(
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
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
):
    """Route to discard a Server."""
    command = DeleteServerCommand(id=id)
    command_bus.register(
        command=DeleteServerCommand,
        handler=DeleteServerCommandHandler(
            repository=repository, message_bus=message_bus
        ),
    )
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Server has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
