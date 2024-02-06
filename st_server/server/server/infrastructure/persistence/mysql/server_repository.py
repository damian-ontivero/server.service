from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from st_server.server.server.domain.server import Server
from st_server.server.server.domain.server_repository import (
    FILTER_OPERATOR_MAPPER,
    ServerRepository,
)
from st_server.server.server.infrastructure.persistence.mysql.credential import (
    CredentialDbModel,
)
from st_server.server.server.infrastructure.persistence.mysql.server import (
    ServerDbModel,
)
from st_server.server.server.infrastructure.persistence.mysql.server_application import (
    ServerApplicationDbModel,
)
from st_server.shared.domain.repository_response import RepositoryResponse


def _build_filter(filter: dict):
    for attr, criteria in filter.items():
        if hasattr(ServerDbModel, attr):
            for op, val in criteria.items():
                if isinstance(val, dict):
                    for k, v in val.items():
                        return (
                            func.json_extract(
                                getattr(ServerDbModel, attr),
                                f"$.{k}",
                            )
                            == v
                        )
                else:
                    return FILTER_OPERATOR_MAPPER[op](
                        ServerDbModel,
                        attr,
                        val,
                    )


def _build_sort(sort: list[dict]):
    for criteria in sort:
        for attr, order in criteria.items():
            if hasattr(ServerDbModel, attr):
                return getattr(getattr(ServerDbModel, attr), order)()


class ServerRepositoryImpl(ServerRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        filter: dict | None = None,
        and_filter: list[dict] | None = None,
        or_filter: list[dict] | None = None,
        sort: list[dict] | None = None,
    ) -> RepositoryResponse:
        if limit is None:
            limit = 0
        if offset is None:
            offset = 0
        if filter is None:
            filter = {}
        if and_filter is None:
            and_filter = []
        if or_filter is None:
            or_filter = []
        if sort is None:
            sort = []
        with self._session as session:
            query = session.query(ServerDbModel)
            if filter:
                query = query.filter(_build_filter(filter))
            if and_filter:
                query = query.filter(
                    and_(*[_build_filter(_and) for _and in and_filter])
                )
            if or_filter:
                query = query.filter(
                    or_(*[_build_filter(_or) for _or in or_filter])
                )
            if sort:
                query = query.order_by(_build_sort(sort))
            total = query.count()
            query = query.limit(limit or total)
            query = query.offset(offset)
            servers = query.all()
            return RepositoryResponse(
                total=total,
                items=[
                    Server.from_primitive_values(
                        id=server.id,
                        name=server.name,
                        cpu=server.cpu,
                        ram=server.ram,
                        hdd=server.hdd,
                        environment=server.environment,
                        operating_system=server.operating_system,
                        credentials=[
                            credential.to_dict()
                            for credential in server.credentials
                        ],
                        applications=[
                            application.to_dict()
                            for application in server.applications
                        ],
                        status=server.status,
                        discarded=server.discarded,
                    )
                    for server in servers
                ],
            )

    def find_by_id(self, id: int) -> Server | None:
        with self._session as session:
            server = (
                session.query(ServerDbModel)
                .filter(ServerDbModel.id == id)
                .first()
            )
            if server is not None:
                return Server.from_primitive_values(
                    id=server.id,
                    name=server.name,
                    cpu=server.cpu,
                    ram=server.ram,
                    hdd=server.hdd,
                    environment=server.environment,
                    operating_system=server.operating_system,
                    credentials=[
                        credential.to_dict()
                        for credential in server.credentials
                    ],
                    applications=[
                        application.to_dict()
                        for application in server.applications
                    ],
                    status=server.status,
                    discarded=server.discarded,
                )
            return None

    def add(self, aggregate: Server) -> None:
        with self._session as session:
            session.add(
                ServerDbModel(
                    id=aggregate.id.value,
                    name=aggregate.name,
                    cpu=aggregate.cpu,
                    ram=aggregate.ram,
                    hdd=aggregate.hdd,
                    environment=aggregate.environment.value,
                    operating_system=aggregate.operating_system.__dict__,
                    credentials=[
                        CredentialDbModel(
                            id=credential.id.value,
                            server_id=credential.server_id.value,
                            connection_type=credential.connection_type.value,
                            username=credential.username,
                            password=credential.password,
                            local_ip=credential.local_ip,
                            local_port=credential.local_port,
                            public_ip=credential.public_ip,
                            public_port=credential.public_port,
                            discarded=credential.discarded,
                        )
                        for credential in aggregate.credentials
                    ],
                    applications=[
                        ServerApplicationDbModel(
                            server_id=application.server_id.value,
                            application_id=application.application_id.value,
                            install_dir=application.install_dir,
                            log_dir=application.log_dir,
                        )
                        for application in aggregate.applications
                    ],
                    status=aggregate.status.value,
                    discarded=aggregate.discarded,
                )
            )
            session.commit()

    def update(self, aggregate: Server) -> None:
        with self._session as session:
            session.query(ServerDbModel).filter(
                ServerDbModel.id == aggregate.id.value
            ).update(
                {
                    ServerDbModel.name: aggregate.name,
                    ServerDbModel.cpu: aggregate.cpu,
                    ServerDbModel.ram: aggregate.ram,
                    ServerDbModel.hdd: aggregate.hdd,
                    ServerDbModel.environment: aggregate.environment.value,
                    ServerDbModel.operating_system: aggregate.operating_system.__dict__,
                    ServerDbModel.status: aggregate.status.value,
                    ServerDbModel.discarded: aggregate.discarded,
                }
            )
            session.commit()

    def delete_by_id(self, id: int) -> None:
        with self._session as session:
            session.query(ServerDbModel).filter(
                ServerDbModel.id == id
            ).delete()
            session.commit()
