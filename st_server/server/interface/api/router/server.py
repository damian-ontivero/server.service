"""Server router."""

import json
import configparser
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError

from st_server.server.application.dto.server import (
    ServerCreateDto,
    ServerReadDto,
    ServerUpdateDto,
)
from st_server.server.application.query.server.server_query import (
    ServerQuery,
)
from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.repository.server_repository import (
    ServerRepositoryImpl,
)
from st_server.shared.application.exception.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)
from st_server.server.application.command.server.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.command.server.update.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.command.server.delete.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.command.server.add.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.command.server.update.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.server.application.command.server.delete.delete_server_command_handler import (
    DeleteServerCommandHandler,
)


router = APIRouter()
auth_scheme = HTTPBearer()

config = configparser.ConfigParser()
config.read("st_server/config.ini")

rabbitmq_host = config.get("rabbitmq", "host")
rabbitmq_port = config.getint("rabbitmq", "port")
rabbitmq_user = config.get("rabbitmq", "user")
rabbitmq_pass = config.get("rabbitmq", "pass")


def get_db_session():
    """Yields a database session."""
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_repository(session: db.SessionLocal = Depends(get_db_session)):
    """Yields a server repository."""
    yield ServerRepositoryImpl(session=session)


def get_message_bus():
    """Yields a message bus."""
    yield RabbitMQMessageBus(
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass,
    )


def get_query(
    repository: ServerRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yields a server query."""
    yield ServerQuery(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[ServerReadDto])
def get_all(
    _limit: int = Query(default=25),
    _offset: int = Query(default=0),
    _filter: str = Query(default="{}"),
    _and_filter: str | None = Query(default="[]"),
    _or_filter: str | None = Query(default="[]"),
    _sort: str | None = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    query: ServerQuery = Depends(get_query),
):
    """Route to get all servers."""
    try:
        servers = query.find_many(
            _limit=_limit,
            _offset=_offset,
            _filter=json.loads(_filter),
            _and_filter=json.loads(_and_filter),
            _or_filter=json.loads(_or_filter),
            _sort=json.loads(_sort),
            access_token=authorization.credentials,
        )
        if not servers._total == 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return JSONResponse(
            content=jsonable_encoder(obj=servers),
            status_code=status.HTTP_200_OK,
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except PaginationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except SortError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except FilterError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/{id}", response_model=ServerReadDto)
def get(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    query: ServerQuery = Depends(get_query),
):
    """Route to get a server by id."""
    try:
        server = query.find_one(id=id, access_token=authorization.credentials)
        return JSONResponse(content=jsonable_encoder(obj=server))
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=ServerReadDto)
def create(
    server_in: ServerCreateDto,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ServerRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Route to create a server."""
    try:
        command = AddServerCommand(
            name=server_in.name,
            cpu=server_in.cpu,
            ram=server_in.ram,
            hdd=server_in.hdd,
            environment=server_in.environment,
            operating_system=server_in.operating_system,
            credentials=server_in.credentials,
            applications=server_in.applications,
        )
        AddServerCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command=command)
        return JSONResponse(
            content=jsonable_encoder(obj=command),
            status_code=status.HTTP_201_CREATED,
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except TypeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.put("/{id}", response_model=ServerReadDto)
def update(
    id: str,
    server_in: ServerUpdateDto,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ServerRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Route to update a server."""
    try:
        command = UpdateServerCommand(
            id=id,
            name=server_in.name,
            cpu=server_in.cpu,
            ram=server_in.ram,
            hdd=server_in.hdd,
            environment=server_in.environment,
            operating_system=server_in.operating_system,
            credentials=server_in.credentials,
            applications=server_in.applications,
            status=server_in.status,
        )
        UpdateServerCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command=command)
        return JSONResponse(
            content=jsonable_encoder(obj=command),
            status_code=status.HTTP_200_OK,
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except TypeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{id}")
def discard(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ServerRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Route to discard a server."""
    try:
        command = DeleteServerCommand(
            id=id, access_token=authorization.credentials
        )
        DeleteServerCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command=command)
        return JSONResponse(
            content=jsonable_encoder(
                obj={"message": "The server has been deleted"}
            ),
            status_code=status.HTTP_200_OK,
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
