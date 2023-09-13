"""
Builds and returns a SQLAlchemy engine object for connecting to a PostgreSQL database.
"""
from os import environ
from sqlalchemy import create_engine, exc, URL


def build_engine():
    """
    Builds and returns a SQLAlchemy engine object for connecting to a PostgreSQL database.

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy engine object for connecting to the database.

    Raises:
        None

    """
    try:
        connction_url = URL.create(
            "postgresql+psycopg2",
            username=environ.get("POSTGRES_USER"),
            password=environ.get("POSTGRES_PASSWORD"),
            host="pdb",
            database=environ.get("POSTGRES_DB"),
            port=5432,
        )
        return create_engine(connction_url)
    # pylint: disable=broad-exception-caught
    except exc.OperationalError as err:
        print("OperationalError: ", err)
        return None


engine = build_engine()
