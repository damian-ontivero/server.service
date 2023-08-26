"""Server router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError

from st_server.server.application.services.server import ServerService
from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.repositories.server_repository import (
    ServerRepositoryImpl,
)
from st_server.server.interface.api.query_parameters.server import (
    ServerQueryParameter,
)
from st_server.server.interface.api.schemas.server import (
    ServerCreate,
    ServerRead,
    ServerUpdate,
)
from st_server.shared.application.exceptions import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)

router = APIRouter()
auth_scheme = HTTPBearer()


def get_db_session():
    """Yields a database session."""
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_server_repository(session: db.SessionLocal = Depends(get_db_session)):
    """Yields a Server repository."""
    yield ServerRepositoryImpl(session=session)


def get_message_bus():
    """Yields a message bus."""
    yield RabbitMQMessageBus(
        host="localhost", port=5672, username="admin", password="admin"
    )


def get_server_service(
    repository: ServerRepositoryImpl = Depends(get_server_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yields a Server service."""
    yield ServerService(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[ServerRead])
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    sort: list[str] | None = Query(default=None),
    filter: ServerQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    server_service: ServerService = Depends(get_server_service),
):
    """Route to get all Servers."""
    try:
        servers = server_service.find_many(
            fields=fields,
            limit=limit,
            offset=offset,
            sort=sort,
            **filter.model_dump(exclude_none=True),
            access_token=authorization.credentials,
        )
        if not servers._items:
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


@router.get("/{id}", response_model=ServerRead)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    server_service: ServerService = Depends(get_server_service),
):
    """Route to get a Server by id."""
    try:
        server = server_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )
        return JSONResponse(content=jsonable_encoder(obj=server))
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=ServerRead)
def create(
    server_in: ServerCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    server_service: ServerService = Depends(get_server_service),
):
    """Route to create a Server."""
    try:
        server = server_service.add_one(
            data=server_in.model_dump(exclude_none=True),
            access_token=authorization.credentials,
        )
        return JSONResponse(
            content=jsonable_encoder(obj=server),
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


@router.put("/{id}", response_model=ServerRead)
def update(
    id: str,
    server_in: ServerUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    server_service: ServerService = Depends(get_server_service),
):
    """Route to update a Server."""
    try:
        server = server_service.update_one(
            id=id,
            data=server_in.model_dump(exclude_none=True),
            access_token=authorization.credentials,
        )
        return JSONResponse(
            content=jsonable_encoder(obj=server),
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
    server_service: ServerService = Depends(get_server_service),
):
    """Route to discard a Server."""
    try:
        server_service.discard_one(
            id=id, access_token=authorization.credentials
        )
        return JSONResponse(
            content=jsonable_encoder(obj={"message": "Server deleted"}),
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
