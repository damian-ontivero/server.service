# Introduction 
The goal of this project is to learn and practice software architecture.
At the moment contains:
- Stack:
  - Python
  - FastAPI
  - SQLAlchemy
  - Alembic
  - MySQL
  - RabbitMQ

- Dessign patterns:
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
server.domain/
├── st_server/
|   ├── __init__.py
|   ├── application/
|   │   ├── __init__.py
|   |   ├── aggregate/                                     One package per aggregate
|   |   |   ├── __init__.py
|   |   |   ├── command/                                   Commands are used to perform actions that modify the aggregate
|   |   |   |   ├── __init__.py
|   |   |   |   ├── command.py                             Command that represents the action to be performed
|   |   |   |   └── command_handler.py                     Command handler that executes the command and mutates the aggregate
|   |   |   └── query/                                     Queries are used for retrieving data or performing complex searches
|   |   |        ├── __init__.py
|   |   |        ├── query.py                              Query that represents the search to be performed
|   |   |        └── query_handler.py                      Query handler that executes the query
|   |   └── command_bus/
|   |       ├── __init__.py
|   |       └── command_bus.py                             Command bus that invokes the command handler
|   │
|   ├── domain/
|   │   ├── __init__.py
|   |   └── aggregate/                                     One package per aggregate
|   |       ├── __init__.py
|   |       ├── root_entity.py                             The root entity of the aggregate
|   |       ├── other_entity.py                            Other entities of the aggregate
|   |       ├── value_object.py                            Value object of the aggregate
|   |       ├── factory.py                                 Factory to build and rebuild the aggregate
|   |       └── repository.py                              Abstract repository for the aggregate
|   │
|   ├── infrastructure/
|   │   ├── __init__.py
|   |   ├── message_bus/
|   |   |   ├── __init__.py
|   |   |   └── rabbitmq_message_bus.py
|   |   |
|   |   ├── persistence/
|   |   |   ├── __init__.py
|   |   |   └── mysql/                                         One package per persistence technology
|   |   |       ├── __init__.py
|   |   |       └── aggregate/                                 One package per aggregate
|   |   |           ├── __init__.py
|   |   |           ├── model_root_entity.py
|   |   |           ├── model_other_entity.py
|   |   |           └── repository_impl.py                     Repository implementation
|   |   |
|   |   └── ui/
|   |       ├── __init__.py
|   |       └── api/                                         One package per persistence technology
|   |           ├── __init__.py
|   |           ├── router
|   |           |    ├── __init__.py
|   |           |    └── aggregate.py                                 One router per aggregate
|   |           ├── exception.py
|   |           └── main.py
|   │
|   └── interface/
|       ├── __init__.py
|       └── aggregate/                                     One package per aggregate
|           ├── __init__.py
|           ├── controller/                                Entry points
|           |   ├── __init__.py
|           |   ├── command_controller.py
|           |   └── query_controller.py
|           └── dto/                                       Data transfer object to represent the data of the aggregate
|               ├── __init__.py
|               └── aggregate_dto.py
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