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
from st_server.context.server.infrastructure.mysql.repository.operating_system_repository import (
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
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_operating_system_repository(
    session: db.SessionLocal = Depends(get_session),
):
    yield OperatingSystemRepository(session=session)


def get_message_bus():
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
    yield OperatingSystemService(
        repository=repository, message_bus=message_bus
    )


@router.get("", response_model=list[OperatingSystemRead])
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    sort: list[str] | None = Query(default=None),
    filter: ServerQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    operating_system_service: OperatingSystemService = Depends(
        get_operating_system_service
    ),
):
    try:
        operating_systems = operating_system_service.find_many(
            fields=fields,
            limit=limit,
            offset=offset,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )
        if not operating_systems.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        base_url = request.base_url
        link = ""
        if operating_systems.prev_offset:
            prev_offset = f'<{base_url}server/operating-systems?limit={operating_systems.limit}&offset={operating_systems.prev_offset}>; rel="prev", '
            link += prev_offset
        if operating_systems.next_offset:
            next_offset = f'<{base_url}server/operating-systems?limit={operating_systems.limit}&offset={operating_systems.next_offset}>; rel="next", '
            link += next_offset
        if operating_systems.last_offset:
            last_offset = f'<{base_url}server/operating-systems?limit={operating_systems.limit}&offset={operating_systems.last_offset}>; rel="last", '
            link += last_offset
        if operating_systems.first_offset:
            first_offset = f'<{base_url}server/operating-systems?limit={operating_systems.limit}&offset={operating_systems.first_offset}>; rel="first"'
            link += first_offset
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
                obj={"message": "OperatingSystem deleted"}
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
