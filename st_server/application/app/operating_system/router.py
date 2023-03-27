"""Doc."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.application.app.operating_system.schema import (
    OperatingSystemQueryParams,
)
from st_server.application.helper.filter import FilterFormatError
from st_server.application.helper.pagination import (
    PageLessThanOne,
    PageNotAnInteger,
    PerPageLessThanZero,
    PerPageNotAnInteger,
)
from st_server.application.helper.sort import SortFormatError
from st_server.application.service.operating_system import (
    OperatingSystemService,
)
from st_server.domain.operating_system import (
    OperatingSystem,
    OperatingSystemCreate,
    OperatingSystemNameAlreadyExists,
    OperatingSystemNotFound,
    OperatingSystemUpdate,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("")
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: OperatingSystemQueryParams = Depends(),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
):
    """Doc."""
    try:
        operating_systems = OperatingSystemService.find_many(
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
            prev_page = '<{0}server/operating-systems?per_page={1}&page={2}>; rel="prev", '.format(
                base_url,
                operating_systems.per_page,
                operating_systems.prev_page,
            )
            link += prev_page

        if operating_systems.next_page:
            next_page = '<{0}server/operating-systems?per_page={1}&page={2}>; rel="next", '.format(
                base_url,
                operating_systems.per_page,
                operating_systems.next_page,
            )
            link += next_page

        if operating_systems.last_page:
            last_page = f'<{0}server/operating-systems?per_page={1}&page={2}>; rel="last", '.format(
                base_url,
                operating_systems.per_page,
                operating_systems.last_page,
            )
            link += last_page

        if operating_systems.first_page:
            first_page = f'<{0}server/operating-systems?per_page={1}&page={2}>; rel="first"'.format(
                base_url,
                operating_systems.per_page,
                operating_systems.first_page,
            )
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(obj=operating_systems.items)
        )
        response.headers["Link"] = link

        return response

    except PageLessThanOne as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except PageNotAnInteger as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except PerPageLessThanZero as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except PerPageNotAnInteger as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except SortFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except FilterFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/{id_}", response_model=OperatingSystem)
def get(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        operating_system = OperatingSystemService.find_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=operating_system))

    except OperatingSystemNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=OperatingSystem)
def create(
    operating_system_in: OperatingSystemCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        operating_system = OperatingSystemService.add_one(
            operating_system_dto=operating_system_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=operating_system))

    except OperatingSystemNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put("/{id_}", response_model=OperatingSystem)
def update(
    id_: int,
    operating_system_in: OperatingSystemUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        operating_system = OperatingSystemService.update_one(
            id_=id_,
            operating_system_dto=operating_system_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=operating_system))

    except OperatingSystemNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except OperatingSystemNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete("/{id_}", response_model=OperatingSystem)
def delete(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        operating_system = OperatingSystemService.delete_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=operating_system))

    except OperatingSystemNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
