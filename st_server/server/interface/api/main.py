"""API module."""

from fastapi import FastAPI, Request
from fastapi.middleware import cors
from fastapi.responses import JSONResponse

from st_server.server.interface.api.exception import (
    EXCEPTION_TO_HTTP_STATUS_CODE,
)
from st_server.server.interface.api.router import application, server

app = FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    router=application.router,
    prefix="/server/applications",
    tags=["Application"],
)

app.include_router(
    router=server.router,
    prefix="/server/servers",
    tags=["Server"],
)


@app.exception_handler(Exception)
def exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        content={"message": str(exception)},
        status_code=EXCEPTION_TO_HTTP_STATUS_CODE[exception.__class__],
    )
