"""SQLAlchemy mysql session."""

from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def get_config() -> ConfigParser:
    """Returns a config parser."""

    config = ConfigParser()
    config.read("st_server/config.ini")

    return config


def get_session() -> Session:
    """Returns a mysql session."""

    config = get_config()

    db_user = config.get("database", "user")
    db_pass = config.get("database", "pass")
    db_host = config.get("database", "host")
    db_port = config.getint("database", "port")
    db_name = config.get("database", "database")
    db_pool_size = config.getint("database", "pool_size")
    db_pool_pre_ping = config.getboolean("database", "pool_pre_ping")
    db_auto_commit = config.getboolean("database", "autocommit")
    db_verbose = config.getboolean("database", "verbose")

    database_uri = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        db_user, db_pass, db_host, db_port, db_name
    )

    engine = create_engine(
        database_uri,
        pool_size=db_pool_size,
        pool_pre_ping=db_pool_pre_ping,
        echo=db_verbose,
    )

    return sessionmaker(bind=engine, autocommit=db_auto_commit)


class Base(DeclarativeBase):
    pass
