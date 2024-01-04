from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from st_server.server.infrastructure.ui.api.exception import (
    EXCEPTION_TO_HTTP_STATUS_CODE,
)
from st_server.server.infrastructure.ui.api.router import application, server

app = FastAPI(
    title="ServerTree - Server domain",
    description="All the endpoints to interact with the Server domain.",
    version="0.1.0",
)

# Routers
app.include_router(router=application.router)
app.include_router(router=server.router)


# Setups the exception handler
@app.exception_handler(Exception)
def exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        content={"message": str(exception)},
        status_code=EXCEPTION_TO_HTTP_STATUS_CODE.get(
            exception.__class__, 500
        ),
    )
