from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_application_query_handler import (
    FindManyApplicationQueryHandler,
)
from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.server.server.application.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.server.application.query.find_many_server_query_handler import (
    FindManyServerQueryHandler,
)
from st_server.server.server.application.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.server.application.query.find_one_server_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.shared.infrastructure.bus.query.in_memory_query_bus import (
    InMemoryQueryBus,
)
from st_server.shared.infrastructure.ui.api.dependency import (
    get_application_repository,
    get_server_repository,
)

QUERY_HANDLER_MAPPING = {
    FindManyApplicationQuery: FindManyApplicationQueryHandler(
        repository=get_application_repository()
    ),
    FindOneApplicationQuery: FindOneApplicationQueryHandler(
        repository=get_application_repository()
    ),
    FindManyServerQuery: FindManyServerQueryHandler(
        repository=get_server_repository()
    ),
    FindOneServerQuery: FindOneServerQueryHandler(
        repository=get_server_repository()
    ),
}

for query, handler in QUERY_HANDLER_MAPPING.items():
    InMemoryQueryBus().register(query, handler)
