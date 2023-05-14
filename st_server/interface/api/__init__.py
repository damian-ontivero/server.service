"""API module."""

from fastapi import FastAPI
from fastapi.middleware import cors

from st_server.interface.api.application.router import (
    router as application_router,
)

# from st_server.interface.api.connection_type.router import (
#     router as connection_type_router,
# )
# from st_server.interface.api.environment.router import (
#     router as environment_router,
# )
# from st_server.interface.api.operating_system.router import (
#     router as operating_system_router,
# )
from st_server.interface.api.server.router import router as server_router

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
    router=application_router,
    prefix="/server/applications",
    tags=["Application"],
)

# app.include_router(
#     router=connection_type_router,
#     prefix="/server/connection-types",
#     tags=["Connection Type"],
# )

# app.include_router(
#     router=environment_router,
#     prefix="/server/environments",
#     tags=["Environment"],
# )

# app.include_router(
#     router=operating_system_router,
#     prefix="/server/operating-systems",
#     tags=["Operating System"],
# )

app.include_router(
    router=server_router,
    prefix="/server/servers",
    tags=["Server"],
)
