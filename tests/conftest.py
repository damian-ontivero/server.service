"""Config file for pytest."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def mock_session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="session", autouse=True)
def test_db(mock_session):
    from st_server.server.infrastructure.persistence.mysql.session import Base

    Base.metadata.create_all(bind=mock_session.get_bind())
    yield
    Base.metadata.drop_all(bind=mock_session.get_bind())
