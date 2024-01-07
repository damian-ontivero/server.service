import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from st_server.server.application.server.command.discard_server_command import (
    DiscardServerCommand,
)
from st_server.server.application.server.command.discard_server_command_handler import (
    DiscardServerCommandHandler,
)
from st_server.server.application.server.command.modify_server_command import (
    ModifyServerCommand,
)
from st_server.server.application.server.command.modify_server_command_handler import (
    ModifyServerCommandHandler,
)
from st_server.server.application.server.command.register_server_command import (
    RegisterServerCommand,
)
from st_server.server.application.server.command.register_server_command_handler import (
    RegisterServerCommandHandler,
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
from st_server.server.infrastructure.persistence.mysql.server.server_repository import (
    ServerRepositoryImpl,
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

router = APIRouter(prefix="/server/servers", tags=["Server"])
auth_scheme = HTTPBearer()


def get_mysql_repository(session: Session = Depends(get_mysql_session)):
    return ServerRepositoryImpl(session)


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str = Query(default="[]"),
    or_filter: str = Query(default="[]"),
    sort: str = Query(default="[]"),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
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
        content=jsonable_encoder(obj=servers),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ServerDto)
def get(
    id: str,
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    query = FindOneServerQuery(id=id)
    handler = FindOneServerQueryHandler(repository=repository)
    server = handler.handle(query)
    return JSONResponse(
        content=jsonable_encoder(obj=server), status_code=status.HTTP_200_OK
    )


@router.post("", response_model=ServerDto)
def create(
    command: RegisterServerCommand,
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command_bus.register(
        command=command,
        handler=RegisterServerCommandHandler(
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
    command: ModifyServerCommand,
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command.id = id
    command_bus.register(
        command=command,
        handler=ModifyServerCommandHandler(
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
    command_bus: CommandBus = Depends(get_command_bus),
    repository: ServerRepositoryImpl = Depends(get_mysql_repository),
    message_bus: RabbitMQMessageBus = Depends(get_rabbitmq_message_bus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command = DiscardServerCommand(id=id)
    command_bus.register(
        command=command,
        handler=DiscardServerCommandHandler(
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
