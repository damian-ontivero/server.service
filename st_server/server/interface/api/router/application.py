"""Application router."""

import json
import configparser
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.dto.application import (
    ApplicationCreateDto,
    ApplicationReadDto,
    ApplicationUpdateDto,
)
from st_server.server.application.query.application.application_query import (
    ApplicationQuery,
)
from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.repository.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.shared.application.exception.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)
from st_server.server.application.command.application.add.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.command.application.update.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.command.application.delete.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.command.application.add.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from st_server.server.application.command.application.update.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
from st_server.server.application.command.application.delete.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)
from st_server.shared.application.response.query_response import QueryResponse


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
    """Yields an application repository."""
    yield ApplicationRepositoryImpl(session=session)


def get_message_bus():
    """Yields a message bus."""
    yield RabbitMQMessageBus(
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass,
    )


def get_query(
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yields an application query."""
    yield ApplicationQuery(repository=repository, message_bus=message_bus)


@router.get("", response_model=QueryResponse)
def get_all(
    _limit: int = Query(default=25),
    _offset: int = Query(default=0),
    _filter: str = Query(default="{}"),
    _and_filter: str | None = Query(default="[]"),
    _or_filter: str | None = Query(default="[]"),
    _sort: str | None = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    query: ApplicationQuery = Depends(get_query),
):
    """Route to get all applications."""
    try:
        applications = query.find_many(
            _limit=_limit,
            _offset=_offset,
            _filter=json.loads(_filter),
            _and_filter=json.loads(_and_filter),
            _or_filter=json.loads(_or_filter),
            _sort=json.loads(_sort),
            access_token=authorization.credentials,
        )
        if applications._total == 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return JSONResponse(
            content=jsonable_encoder(obj=applications),
            status_code=status.HTTP_200_OK,
        )
    except AuthenticationError as e:
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


@router.get("/{id}", response_model=ApplicationReadDto)
def get(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    query: ApplicationQuery = Depends(get_query),
):
    """Route to get an application by id."""
    try:
        application = query.find_one(
            id=id, access_token=authorization.credentials
        )
        return JSONResponse(
            content=jsonable_encoder(obj=application),
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


@router.post("", response_model=ApplicationReadDto)
def create(
    application_in: ApplicationCreateDto,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Route to create an application."""
    try:
        command = AddApplicationCommand(
            name=application_in.name,
            version=application_in.version,
            architect=application_in.architect,
        )
        application = AddApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command=command)
        return JSONResponse(
            content=jsonable_encoder(obj=application),
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


@router.put("/{id}", response_model=ApplicationReadDto)
def update(
    id: str,
    application_in: ApplicationUpdateDto,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Route to update an application."""
    try:
        command = UpdateApplicationCommand(
            id=id,
            name=application_in.name,
            version=application_in.version,
            architect=application_in.architect,
        )
        application = UpdateApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command=command)
        return JSONResponse(
            content=jsonable_encoder(obj=application),
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
def delete(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repository: ApplicationRepositoryImpl = Depends(get_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Route to discard an application."""
    try:
        command = DeleteApplicationCommand(id=id)
        DeleteApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command=command)
        return JSONResponse(
            content=jsonable_encoder(
                obj={"message": "The application has been deleted"}
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
