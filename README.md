# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)

# Architecture

project/
├── migrations/
|   ├── __init__.py
|   └── versions/
|       ├── __init__.py
|       └── 0001_initial.py
|
├── st_server/
|   ├── __init__.py
|   ├── application/
|   │   ├── __init__.py
|   |   └── aggregate/                                              One package per aggregate
|   |       ├── __init__.py
|   |       ├── commands/                                           Commands are used to perform actions that modify the aggregate
|   |       |   ├── __init__.py
|   |       │   └── command/                                        One package per command
|   |       │       ├── __init__.py
|   |       │       ├── command.py                                  Command that represents the action to be performed
|   |       │       └── command_handle.py                           Command handler that executes the command and mutates the aggregate
|   |       ├── queries/                                            Queries are used to read data from the 
|   |       |   ├── __init__.py
|   |       │   └── query.py                                        Queries are used for retrieving data or performing complex searches
|   |       └── dtos/
|   |           ├── __init__.py
|   |           └── dto.py                                          DTO to represent the data of the aggregate
|   │
|   ├── domain/
|   │   ├── __init__.py
|   |   └── aggregate/                                              One package per aggregate
|   |       ├── entities/
|   |       |   ├── __init__.py
|   |       |   ├── root_entity.py                                  The root entity of the aggregate
|   |       │   └── other_entity.py                                 Other entities of the aggregate
|   |       ├── value_objects/
|   |       |   ├── __init__.py
|   |       │   └── value_object.py                                 Value object of the aggregate
|   |       ├── factories/
|   |       |   ├── __init__.py
|   |       │   └── aggregate.py                                    Factory to build and rebuild the aggregate
|   |       └── repositories
|   |           ├── __init__.py
|   |           └── aggregate.py                                    Abstract repository for the aggregate
|   │
|   ├── infrastructure/
|   │   ├── __init__.py
|   |   ├── messaging/
|   |   |   ├── __init__.py
|   |   |   ├── in_memory.py
|   |   |   └── rabbitmq.py
|   |   └── aggregate/                                              One package per aggregate
|   |       ├── __init__.py
|   |       └── mysql/
|   |           ├── __init__.py
|   |           ├── models/
|   |           |   ├── __init__.py
|   |           |   ├── root_entity.py
|   |           |   └── other_entity.py
|   |           └── repositories/
|   |               ├── __init__.py
|   |               └── aggregate.py
|   │
|   └── interfaces/
|       ├── __init__.py
|       └── controllers/
|           ├── __init__.py
|           └── aggregate/                                          One package per aggregate
|               ├── __init__.py
|               ├── command.py
|               └── query.py
|
├── tests/
|   ├── __init__.py
|   ├── unit/
|   |   ├── __init__.py
|   |   ├── application/
|   |   |   ├── __init__.py
|   |   |   └── aggregate/                                          One package per aggregate
|   |   |       ├── __init__.py
|   |   |       ├── commands/
|   |   |       |   ├── __init__.py
|   |   |       |   └── test_command.py
|   |   |       ├── queries/
|   |   |       |   ├── __init__.py
|   |   |       │   └── test_query.py
|   |   |       └── dtos/
|   |   |           ├── __init__.py
|   |   |           └── test_dto.py
|   |   │
|   |   ├── domain/
|   |   |   ├── __init__.py
|   |   |   └── aggregate/                                          One package per aggregate
|   |   |       ├── entities/
|   |   |       |   ├── __init__.py
|   |   |       |   ├── root_entity.py                              The root entity of the aggregate
|   |   |       │   └── other_entity.py                             Other entities of the aggregate
|   |   |       ├── value_objects/
|   |   |       |   ├── __init__.py
|   |   |       │   └── value_object.py                             Value object of the aggregate
|   |   |       ├── factories/
|   |   |       |   ├── __init__.py
|   |   |       │   └── aggregate.py                                Factory for build and rebuild the aggregate
|   |   |       └── repositories
|   |   |           ├── __init__.py
|   |   |           └── aggregate.py                                Abstract repository for the aggregate
|   |   │
|   |   ├── infrastructure/
|   |   |   ├── __init__.py
|   |   |   ├── messaging/
|   |   |   |   ├── __init__.py
|   |   |   |   ├── in_memory.py
|   |   |   |   └── rabbitmq.py
|   |   |   └── persistence/
|   |   |       ├── __init__.py
|   |   |       └── aggregate/                                      One package per aggregate
|   |   |           ├── __init__.py
|   |   |           └── mysql/
|   |   |               ├── __init__.py
|   |   |               ├── models/
|   |   |               |   ├── __init__.py
|   |   |               |   ├── root_entity.py
|   |   |               |   └── other_entity.py
|   |   |               └── repositories/
|   |   |                   ├── __init__.py
|   |   |                   └── aggregate.py
|   |   │
|   |   └── interfaces/
|   |       ├── __init__.py
|   |       └── controllers/
|   |           ├── __init__.py
|   |           └── aggregate/                                      One package per aggregate
|   |               ├── __init__.py
|   |               ├── command.py
|   |               └── query.py
|   │
|   └── util/
|       ├── __init__.py
|       └── aggregate/                                              One package per aggregate
|           └── factories/
|               ├── __init__.py
|               └── aggregate.py
│
├── .env
├── .env.example
├── .env.example.test
├── alembic.ini
├── poetry.lock
├── pyproject.toml
├── README.md
└── setup.cfg