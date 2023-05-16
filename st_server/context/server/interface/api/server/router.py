"""Server router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.context.server.application.service.server import ServerService
from st_server.context.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.context.server.infrastructure.mysql import db
from st_server.context.server.infrastructure.mysql.server.server_repository import (
    ServerRepository,
)
from st_server.context.server.interface.api.server.query_parameter import (
    ServerQueryParameter,
)
from st_server.context.server.interface.api.server.schema import (
    ServerCreate,
    ServerRead,
    ServerUpdate,
)
from st_server.shared.core.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)

router = APIRouter()
auth_scheme = HTTPBearer()


def get_session():
    """Yield a database session."""
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_server_repository(session: db.SessionLocal = Depends(get_session)):
    """Yield a server repository."""
    yield ServerRepository(session=session)


def get_message_bus():
    """Yield a message bus."""
    yield RabbitMQMessageBus(
        host="localhost",
        port=5672,
        username="admin",
        password="admin",
    )


def get_server_service(
    repository: ServerRepository = Depends(get_server_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yield a server service."""
    yield ServerService(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[ServerRead])
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: ServerQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    server_service: ServerService = Depends(get_server_service),
):
    """Doc."""
    try:
        servers = server_service.find_many(
            fields=fields,
            per_page=per_page,
            page=page,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not servers.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if servers.prev_page:
            prev_page = f'<{base_url}support/servers?per_page={servers.per_page}&page={servers.prev_page}>; rel="prev", '
            link += prev_page

        if servers.next_page:
            next_page = f'<{base_url}support/servers?per_page={servers.per_page}&page={servers.next_page}>; rel="next", '
            link += next_page

        if servers.last_page:
            last_page = f'<{base_url}support/servers?per_page={servers.per_page}&page={servers.last_page}>; rel="last", '
            link += last_page

        if servers.first_page:
            first_page = f'<{base_url}support/servers?per_page={servers.per_page}&page={servers.first_page}>; rel="first"'
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(
                obj=[
                    ServerRead(**server.to_dict()) for server in servers.items
                ]
            )
        )
        response.headers["Link"] = link

        return response

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


@router.get("/{id}", response_model=ServerRead)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    server_service: ServerService = Depends(get_server_service),
):
    """Doc."""
    try:
        server = server_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(obj=ServerRead(**server.to_dict()))
        )

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
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ServerRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        server_service = ServerService(
            repository=repository, message_bus=message_bus
        )

        server = server_service.add_one(
            data=server_in.to_dict(), access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(obj=ServerRead(**server.to_dict())),
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


@router.put("/{id}", response_model=ServerRead)
def update(
    id: str,
    server_in: ServerUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ServerRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        server_service = ServerService(
            repository=repository, message_bus=message_bus
        )

        server = server_service.update_one(
            id=id,
            data=server_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(obj=ServerRead(**server.to_dict())),
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


@router.delete("/{id}")
def discard(
    id: str, authorization: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ServerRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        server_service = ServerService(
            repository=repository, message_bus=message_bus
        )

        server_service.discard_one(
            id=id, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(obj={"message": "User deleted"}),
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
