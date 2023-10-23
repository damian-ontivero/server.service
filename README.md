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

# Project structure
```
src/
├── migrations/
|   ├── __init__.py
|   └── versions/
|       ├── __init__.py
|       └── 0001_initial.py
|
├── rt_buildplatf/
|   ├── __init__.py
|   ├── application/
|   │   ├── __init__.py
|   |   └── aggregate/                                          One package per aggregate
|   |       ├── __init__.py
|   |       ├── command/                                        Commands are used to perform actions that modify the aggregate
|   |       |    ├── __init__.py
|   |       |    ├── command.py                                 Command that represents the action to be performed
|   |       |    └── command_handler.py                         Command handler that executes the command and mutates the aggregate
|   |       ├── query/                                          Queries are used for retrieving data or performing complex searches
|   |       |   ├── __init__.py
|   |       |   ├── query.py                                    Query that represents the search to be performed
|   |       │   └── query_handler.py                            Query handler that executes the query
|   |       |   
|   |       └── dto/
|   |           ├── __init__.py
|   |           └── dto.py                                      Data transfer object to represent the data of the aggregate
|   │
|   ├── domain/
|   │   ├── __init__.py
|   |   └── aggregate/                                          One package per aggregate
|   |       ├── __init__.py
|   |       ├── root_entity.py                                  The root entity of the aggregate
|   |       ├── other_entity.py                                 Other entities of the aggregate
|   |       ├── value_object.py                                 Value object of the aggregate
|   |       ├── factory.py                                      Factory to build and rebuild the aggregate
|   |       └── repository.py                                   Abstract repository for the aggregate
|   │
|   ├── infrastructure/
|   │   ├── __init__.py
|   |   ├── bus/
|   |   |   ├── __init__.py
|   |   |   └── rabbitmq.py
|   |   └── persistence/
|   |       ├── __init__.py
|   |       └── mysql/                                          One package per persistence technology
|   |           ├── __init__.py
|   |           ├── aggregate/                                  One package per aggregate
|   |               ├── __init__.py
|   |               ├── model_root_entity.py
|   |               ├── model_other_entity.py
|   |               └── repository.py
|   │
|   └── interface/
|       ├── __init__.py
|       └── controller/                                         API entrypoint
|           ├── __init__.py
|           └── aggregate/                                      One package per aggregate
|               ├── __init__.py
|               ├── command_controller.py
|               └── query_controller.py
|
├── tests/
|   ├── __init__.py
|   ├── unit/
|   |   ├── __init__.py
|   |   ├── application/
|   |   |   ├── __init__.py
|   |   |   └── aggregate/                                      One package per aggregate
|   |   |       ├── __init__.py
|   |   |       ├── command/
|   |   |       |   ├── __init__.py
|   |   |       |   └── test_command.py
|   |   |       ├── query/
|   |   |       |   ├── __init__.py
|   |   |       │   └── test_query.py
|   |   |       └── dto/
|   |   |           ├── __init__.py
|   |   |           └── test_dto.py
|   |   │
|   |   ├── domain/
|   |   |   ├── __init__.py
|   |   |   └── aggregate/                                      One package per aggregate
|   |   |       ├── __init__.py
|   |   |       ├── root_entity.py                              The root entity of the aggregate
|   |   |       ├── other_entity.py                             Other entities of the aggregate
|   |   |       ├── value_object.py                             Value object of the aggregate
|   |   |       ├── factory.py                                  Factory to build and rebuild the aggregate
|   |   |       └── repository.py                               Abstract repository for the aggregate
|   |   │
|   |   ├── infrastructure/
|   |   │   ├── __init__.py
|   |   |   ├── bus/
|   |   |   |   ├── __init__.py
|   |   |   |   └── rabbitmq.py
|   |   |   └── persistence/
|   |   |       ├── __init__.py
|   |   |       └── mysql/                                      One package per persistence technology
|   |   |           ├── __init__.py
|   |   |           ├── aggregate/                              One package per aggregate
|   |   |               ├── __init__.py
|   |   |               ├── model_root_entity.py
|   |   |               ├── model_other_entity.py
|   |   |               └── repository.py
|   |   │
|   |   └── interface/
|   |       ├── __init__.py
|   |       └── controller/
|   |           ├── __init__.py
|   |           └── aggregate/                                  One package per aggregate
|   |               ├── __init__.py
|   |               ├── command_controller.py
|   |               └── query_controller.py
|   │
|   └── util/
|       ├── __init__.py
|       └── aggregate/                                          One package per aggregate
|           └── factory/
|               ├── __init__.py
|               ├── root_entity.py
|               └── value_object.py
│
├── .env
├── .env.example
├── .env.example.test
├── alembic.ini
├── poetry.lock
├── pyproject.toml
├── README.md
└── setup.cfg
```