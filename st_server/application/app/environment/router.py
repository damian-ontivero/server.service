"""Doc."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.application.app.environment.schema import EnvironmentQueryParams
from st_server.application.helper.filter import FilterFormatError
from st_server.application.helper.pagination import (
    PageLessThanOne,
    PageNotAnInteger,
    PerPageLessThanZero,
    PerPageNotAnInteger,
)
from st_server.application.helper.sort import SortFormatError
from st_server.application.service.environment.environment import (
    EnvironmentService,
)
from st_server.domain.environment import (
    Environment,
    EnvironmentCreate,
    EnvironmentNameAlreadyExists,
    EnvironmentNotFound,
    EnvironmentUpdate,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("")
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: EnvironmentQueryParams = Depends(),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
):
    """Doc."""
    try:
        environments = EnvironmentService.find_many(
            per_page=per_page,
            page=page,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not environments.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if environments.prev_page:
            prev_page = '<{0}server/environments?per_page={1}&page={2}>; rel="prev", '.format(
                base_url, environments.per_page, environments.prev_page
            )
            link += prev_page

        if environments.next_page:
            next_page = '<{0}server/environments?per_page={1}&page={2}>; rel="next", '.format(
                base_url, environments.per_page, environments.next_page
            )
            link += next_page

        if environments.last_page:
            last_page = f'<{0}server/environments?per_page={1}&page={2}>; rel="last", '.format(
                base_url, environments.per_page, environments.last_page
            )
            link += last_page

        if environments.first_page:
            first_page = f'<{0}server/environments?per_page={1}&page={2}>; rel="first"'.format(
                base_url,
                environments.per_page,
                environments.first_page,
            )
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(obj=environments.items)
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


@router.get("/{id_}", response_model=Environment)
def get(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        environment = EnvironmentService.find_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=environment))

    except EnvironmentNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=Environment)
def create(
    environment_in: EnvironmentCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        environment = EnvironmentService.add_one(
            environment_dto=environment_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=environment))

    except EnvironmentNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put("/{id_}", response_model=Environment)
def update(
    id_: int,
    environment_in: EnvironmentUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        environment = EnvironmentService.update_one(
            id_=id_,
            environment_dto=environment_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=environment))

    except EnvironmentNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except EnvironmentNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete("/{id_}", response_model=Environment)
def delete(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        environment = EnvironmentService.delete_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=environment))

    except EnvironmentNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
