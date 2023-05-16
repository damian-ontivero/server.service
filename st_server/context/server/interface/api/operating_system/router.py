"""Server router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.context.server.application.service.operating_system import (
    OperatingSystemService,
)
from st_server.context.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.context.server.infrastructure.mysql import db
from st_server.context.server.infrastructure.mysql.operating_system.operating_system_repository import (
    OperatingSystemRepository,
)
from st_server.context.server.interface.api.operating_system.schema import (
    OperatingSystemCreate,
    OperatingSystemRead,
    OperatingSystemUpdate,
)
from st_server.context.server.interface.api.server.query_parameter import (
    ServerQueryParameter,
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


def get_operating_system_repository(
    session: db.SessionLocal = Depends(get_session),
):
    """Yield a operating system repository."""
    yield OperatingSystemRepository(session=session)


def get_message_bus():
    """Yield a message bus."""
    yield RabbitMQMessageBus(
        host="localhost",
        port=5672,
        username="admin",
        password="admin",
    )


def get_operating_system_service(
    repository: OperatingSystemRepository = Depends(
        get_operating_system_repository
    ),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yield a operating system service."""
    yield OperatingSystemService(
        repository=repository, message_bus=message_bus
    )


@router.get("", response_model=list[OperatingSystemRead])
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: ServerQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    operating_system_service: OperatingSystemService = Depends(
        get_operating_system_service
    ),
):
    """Doc."""
    try:
        operating_systems = operating_system_service.find_many(
            fields=fields,
            per_page=per_page,
            page=page,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not operating_systems.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if operating_systems.prev_page:
            prev_page = f'<{base_url}support/operating-systems?per_page={operating_systems.per_page}&page={operating_systems.prev_page}>; rel="prev", '
            link += prev_page

        if operating_systems.next_page:
            next_page = f'<{base_url}support/operating-systems?per_page={operating_systems.per_page}&page={operating_systems.next_page}>; rel="next", '
            link += next_page

        if operating_systems.last_page:
            last_page = f'<{base_url}support/operating-systems?per_page={operating_systems.per_page}&page={operating_systems.last_page}>; rel="last", '
            link += last_page

        if operating_systems.first_page:
            first_page = f'<{base_url}support/operating-systems?per_page={operating_systems.per_page}&page={operating_systems.first_page}>; rel="first"'
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(
                obj=[
                    OperatingSystemRead(**operating_system.to_dict())
                    for operating_system in operating_systems.items
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


@router.get("/{id}", response_model=OperatingSystemRead)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    operating_system_service: OperatingSystemService = Depends(
        get_operating_system_service
    ),
):
    """Doc."""
    try:
        operating_system = operating_system_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=OperatingSystemRead(**operating_system.to_dict())
            )
        )

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )

    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=OperatingSystemRead)
def create(
    operating_system_in: OperatingSystemCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = OperatingSystemRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        operating_system_service = OperatingSystemService(
            repository=repository, message_bus=message_bus
        )

        operating_system = operating_system_service.add_one(
            data=operating_system_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=OperatingSystemRead(**operating_system.to_dict())
            ),
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


@router.put("/{id}", response_model=OperatingSystemRead)
def update(
    id: str,
    operating_system_in: OperatingSystemUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = OperatingSystemRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        operating_system_service = OperatingSystemService(
            repository=repository, message_bus=message_bus
        )

        operating_system = operating_system_service.update_one(
            id=id,
            data=operating_system_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=OperatingSystemRead(**operating_system.to_dict())
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
        repository = OperatingSystemRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        operating_system_service = OperatingSystemService(
            repository=repository, message_bus=message_bus
        )

        operating_system_service.discard_one(
            id=id, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj={"message": "Operating system deleted"}
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
