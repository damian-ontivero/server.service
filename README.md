# Introduction 
The goal of this project is to learn and practice software architecture.
At the moment contains:
- Stack:
  - Python
  - FastAPI
  - SQLAlchemy
  - Alembic
  - MySQL

- Dessign patterns:
  - Domain-Driven Design
    - Factory
    - Repository
    - Value Object
  - Clean Architecture
  - CQRS

# Project structure
```
server.domain/
├── st_server/
|   ├── __init__.py
|   ├── application/
|   │   ├── __init__.py
|   |   └── aggregate/                                One package per aggregate
|   |       ├── __init__.py
|   |       ├── command/                              Performs actions that modify the aggregate
|   |       |   ├── __init__.py
|   |       |   ├── command.py                        Represents the action to be performed
|   |       |   └── command_handler.py                Executes the command and mutates the aggregate
|   |       └── query/                                Retrieves data or performing complex searches
|   |           ├── __init__.py
|   |           ├── query.py                          Query that represents the search to be performed
|   |           └── query_handler.py                  Query handler that executes the query
|   │
|   ├── domain/
|   │   ├── __init__.py
|   |   └── aggregate/                                One package per aggregate
|   |       ├── __init__.py
|   |       ├── root_entity.py                        The root entity of the aggregate
|   |       ├── other_entity.py                       Other entities of the aggregate
|   |       ├── value_object.py                       Value object of the aggregate
|   |       ├── factory.py                            Factory to build and rebuild the aggregate
|   |       └── repository.py                         Abstract repository for the aggregate
|   │
|   ├── infrastructure/
|   │   ├── __init__.py
|   |   ├── bus/
|   |   |   ├── __init__.py
|   |   |   └── rabbitmq.py
|   |   └── persistence/
|   |       ├── __init__.py
|   |       └── mysql/                                One package per persistence technology
|   |           ├── __init__.py
|   |           └── aggregate/                        One package per aggregate
|   |               ├── __init__.py
|   |               ├── root_entity_model.py
|   |               ├── other_entity_model.py
|   |               └── root_entity_repository.py     Concrete repository
|   │
|   ├── presentation/
|   |   ├── __init__.py
|   |   └── aggregate/                                One package per aggregate
|   |       ├── __init__.py
|   |       ├── controller/                           API entrypoint
|   |       |   ├── __init__.py
|   |       |   ├── command_controller.py
|   |       |   └── query_controller.py
|   |       └── dto/
|   |           ├── __init__.py
|   |           └── aggregate_dto.py                  Represents the data of the aggregate
|   |
|   └── interface/
|       ├── __init__.py
|       └── api/
|           ├── __init__.py
|           ├── main.py
|           ├── exception.py
|           └── router/
|               ├── __init__.py
|               └── aggregate.py
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