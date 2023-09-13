"""
    Initial DB seed
"""
from typing import List, Dict
from os import path, environ
from csv import DictReader
from sqlalchemy import text, Engine, URL, create_engine

CSV_FILE_PATH = path.join(path.dirname(__file__), "nimble_contacts_sheet.csv")

CURRENT_FILE_NAME = path.basename(__file__)


def check_seed_exists(engine: Engine):
    """
    Check if a seed exists in the database.

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
            WHERE table_name = 'seeds'
        );
        """
        exec_result = connection.execute(text(query))
        table_exists = exec_result.scalar()
        if table_exists:
            query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM seeds
                    WHERE seed_name = :seed_name
                );
            """
            seed_exists = connection.execute(
                text(query), {"seed_name": CURRENT_FILE_NAME}
            ).scalar()
            return seed_exists


def parse_csv() -> List[Dict[str, str]]:
    """
    Parses a CSV file and returns a list of dictionaries containing the data.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing
        each row in the CSV file. Each dictionary contains the following keys:
            - "first_name" (str): The first name of the person.
            If the value is missing, the default value "Was not provided" is used.
            - "last_name" (str): The last name of the person.
            If the value is missing, the default value "Was not provided" is used.
            - "email" (str): The email address of the person.
            If the value is missing, the default value "Was not provided" is used.
            - "description" (str): A description of the person.
            If the value is missing, the default value "Was not provided" is used.
    """
    try:
        with open(CSV_FILE_PATH, newline="", encoding="utf-8", mode="r") as file:
            seed_data = DictReader(file)
            result = []
            for row in seed_data:
                result.append(
                    {
                        "first_name": row.get("first name", "Was not provided"),
                        "last_name": row.get("last name", "Was not provided"),
                        "email": row.get("email", "Was not provided"),
                        "description": row.get("description", "Was not provided"),
                    }
                )
            return result
    except OSError as err:
        print(err)
        return []


def seed_db(engine):
    """
    Seed the database with data from a CSV file.

    Parameters:
        engine (Engine): The SQLAlchemy engine to connect to the database.

    Returns:
        str: A message indicating that the seeding process is complete.
    """
    data = parse_csv()
    with engine.connect() as connection:
        seed_query: str = "INSERT INTO seeds (seed_name) VALUES (:seed_name);"
        user_query: str = """INSERT INTO users (
            first_name, last_name, email, description)
            VALUES (:first_name, :last_name, :email, :description);
        """

        connection.execute(text(user_query), data)
        connection.execute(
            text(seed_query),
            {
                "seed_name": CURRENT_FILE_NAME,
            },
        )

        connection.commit()
        return "Done"


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
        if check_seed_exists(db_engine):
            pass
        else:
            seed_db(db_engine)
