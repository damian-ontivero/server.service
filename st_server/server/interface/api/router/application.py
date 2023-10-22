"""Application router."""

import configparser
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
    ApplicationCreateDto,
    ApplicationReadDto,
    ApplicationUpdateDto,
)
from st_server.server.application.application.query.application_query import (
    ApplicationQuery,
)
from st_server.server.infrastructure.bus.rabbitmq import RabbitMQMessageBus
from st_server.server.infrastructure.persistence.mysql import session
from st_server.server.infrastructure.persistence.mysql.application.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.shared.application.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)
from st_server.shared.application.query_response import QueryResponse

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
    session = session.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_repository(session: session.SessionLocal = Depends(get_db_session)):
    """Yields an Application repository."""
    yield ApplicationRepositoryImpl(session)


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
    """Yields an Application query."""
    yield ApplicationQuery(repository=repository, message_bus=message_bus)


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str | None = Query(default="[]"),
    or_filter: str | None = Query(default="[]"),
    sort: str | None = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    query: ApplicationQuery = Depends(get_query),
):
    """Route to get all applications."""
    try:
        applications = query.find_many(
            limit=limit,
            offset=offset,
            filter=json.loads(filter),
            and_filter=json.loads(and_filter),
            or_filter=json.loads(or_filter),
            sort=json.loads(sort),
            access_token=authorization.credentials,
        )
        if applications.total == 0:
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
    """Route to get an Application by id."""
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
    """Route to create an Application."""
    try:
        command = AddApplicationCommand(
            name=application_in.name,
            version=application_in.version,
            architect=application_in.architect,
        )
        application = AddApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command)
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
    """Route to update an Application."""
    try:
        command = UpdateApplicationCommand(
            id=id,
            name=application_in.name,
            version=application_in.version,
            architect=application_in.architect,
        )
        application = UpdateApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command)
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
    """Route to delete an Application."""
    try:
        command = DeleteApplicationCommand(id=id)
        DeleteApplicationCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command)
        return JSONResponse(
            content=jsonable_encoder(
                obj={"message": "The Application has been deleted"}
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