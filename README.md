# Introduction 
The goal of this project is to learn and practice software architecture.

### Stack:
- Python
- FastAPI
- SQLAlchemy
- Alembic
- MySQL
- RabbitMQ

### Dessign patterns:
- Domain-Driven Design
  - Aggregate
  - Factory
  - Repository
  - Value Object
- Clean Architecture
- CQRS
- Domain Events

# Project structure
```
server.service/
├── st_server/
|   ├── server/
|   |   ├── __init__.py
|   |   ├── application/
|   |   │   ├── __init__.py
|   |   |   └── aggregate/                                # One package per aggregate
|   |   |       ├── __init__.py
|   |   |       ├── command/                              # Commands are used to perform actions that modify the aggregate
|   |   |       |   ├── __init__.py
|   |   |       |   ├── command.py                        # Command that represents the action to be performed
|   |   |       |   └── command_handler.py                # Command handler that executes the command and mutates the aggregate
|   |   |       ├── dto/                                  # Data transfer object to represent the data of the aggregate
|   |   |       |    ├── __init__.py
|   |   |       |    └── aggregate_dto.py
|   |   |       └── query/                                # Queries are used for retrieving data or performing complex searches
|   |   |            ├── __init__.py
|   |   |            ├── query.py                         # Query that represents the search to be performed
|   |   |            └── query_handler.py                 # Query handler that executes the query
|   |   │
|   |   ├── domain/
|   |   │   ├── __init__.py
|   |   |   └── aggregate/                                # One package per aggregate
|   |   |       ├── __init__.py
|   |   |       ├── root_entity.py                        # The root entity of the aggregate
|   |   |       ├── other_entity.py                       # Other entities of the aggregate
|   |   |       ├── value_object.py                       # Value object of the aggregate
|   |   |       └── repository.py                         # Abstract repository for the aggregate
|   |   │
|   |   └── infrastructure/
|   |       ├── __init__.py
|   |       ├── persistence/
|   |       |   ├── __init__.py
|   |       |   └── mysql/                                # One package per persistence technology
|   |       |       ├── __init__.py
|   |       |       └── aggregate/                        # One package per aggregate
|   |       |           ├── __init__.py
|   |       |           ├── model_root_entity.py          # Database model for the root entity.
|   |       |           ├── model_other_entity.py         # Database model for an other entity.
|   |       |           ├── model_value_object.py         # Database model for a value object .
|   |       |           └── repository_impl.py            # Repository implementation
|   |       └── ui/
|   |           ├── __init__.py
|   |           └── api/                                  # One package per user interface technology
|   |               ├── __init__.py
|   |               ├── router/                           # Definitions of endpoints.
|   |               |   ├── __init__.py
|   |               |   └── aggregate.py                  # One router per aggregate
|   |               ├── dependency.py                     # FastAPI dependency injection.
|   |               ├── exception.py                      # Exception handling for FastAPI.
|   |               └── main.py                           # Main file.
|   |
|   ├── shared/
|   |   ├── __init__.py
|   |   ├── application/
|   |   ├── domain/
|   |   └── infrastructure/
|   |
|   ├── __init__.py
|   └── config.ini                                         # Configuration file.
|
├── .gitignore
├── alembic.ini
├── compose.dev.yaml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
└── setup.cfg
```