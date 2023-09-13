"""
Migration. No rollbacks
"""

import sys
from os import path, environ
from sqlalchemy import text, Engine, URL, create_engine

CURRENT_FILE_NAME = path.basename(__file__)


def create_db_table(engine: Engine, query: str):
    """
    Creates a database table using the provided database engine and query.

    Args:
        engine (Engine): The database engine to use for the connection.
        query (str): The SQL query to create the table.

    Returns:
        None: This function does not return anything.

    Raises:
        None: This function does not raise any exceptions.
    """
    enable_uuid_ossp_query = text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    with engine.connect() as connection:
        connection.execute(enable_uuid_ossp_query)
        connection.execute(text(query))
        return connection.commit()


def create_seeds_table(engine: Engine):
    """
    Create a seeds table in the database if it does not already exist.

    Args:
        engine (Engine): The database engine to use for executing the query.

    Returns:
        None
    """
    query: str = """
    CREATE TABLE IF NOT EXISTS seeds (
        id uuid DEFAULT uuid_generate_v4() PRIMARY KEY, 
        seed_name varchar(255) NOT NULL UNIQUE, created_at timestamp NOT NULL DEFAULT current_timestamp
    );
    """
    return create_db_table(engine, query)


def create_user_table(engine: Engine):
    """
    Create a user table in the database if it does not already exist.

    Parameters:
        engine (Engine): The database engine to use.

    Returns:
        None
    """
    query: str = """
        CREATE TABLE IF NOT EXISTS users (
	        id uuid DEFAULT uuid_generate_v4() PRIMARY KEY, 
	        first_name varchar(45) NOT NULL, 
	        last_name varchar(45) NOT NULL, 
	        email varchar(254) NOT NULL UNIQUE, 
	        description varchar(500)
        ); 
            """
    return create_db_table(engine, query)


def create_migrations_table(engine):
    """
    Inserts the migration name into the 'migrations' table.

    Parameters:
        engine (Engine): The database engine to use for the connection.

    Returns:
        Any: The result of executing the query.
    """
    query: str = """
    CREATE TABLE IF NOT EXISTS migrations (
        id uuid DEFAULT uuid_generate_v4() PRIMARY KEY, 
        migration_name varchar(255) NOT NULL UNIQUE, created_at timestamp NOT NULL DEFAULT current_timestamp
    );
    """
    return create_db_table(engine, query)


def migration_complete(engine):
    """
    Executes the migration_complete function.

    Args:
        engine (Engine): The database engine to use for the connection.

    Returns:
        scalar: The result of the executed query.
    """
    with engine.connect() as connection:
        query: str = "INSERT INTO migrations (migration_name) VALUES (:migration_name);"

        connection.execute(
            text(query),
            {
                "migration_name": CURRENT_FILE_NAME,
            },
        )
        connection.commit()
        return "Done"


def check_migration_exists(engine: Engine):
    """
    Check if a migration exists in the database.

    Parameters:
        engine (connection): The database connection.

    Returns:
        bool: True if the seed exists, False otherwise.
    """
    with engine.connect() as connection:
        query: str = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'migrations'
        );
        """

        exec_result = connection.execute(text(query))
        table_exists = exec_result.scalar()

        if table_exists:
            query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM migrations
                    WHERE migration_name = :migration_name
                );
            """

            migration_exists = connection.execute(
                text(query), {"migration_name": CURRENT_FILE_NAME}
            ).scalar()
            return migration_exists


if __name__ == "__main__":
    connction_url = URL.create(
        "postgresql+psycopg2",
        username=environ.get("POSTGRES_USER"),
        password=environ.get("POSTGRES_PASSWORD"),
        host="pdb",
        database=environ.get("POSTGRES_DB"),
        port=5432,
    )
    db_engine = create_engine(connction_url)
    
    if db_engine:
        if not check_migration_exists(db_engine):
            try:
                proc_pipe = [
                    create_migrations_table,
                    create_seeds_table,
                    create_user_table,
                ]
                migration_result = list(map(lambda f: f(db_engine), proc_pipe))
                print(migration_complete(db_engine))
            except OSError as e:
                print("Migration error", e)
                sys.exit(0)
        else:
            pass
