"""
    Initial DB seed
"""
from typing import List, Dict
from os import environ, path
from csv import DictReader
from sqlalchemy import create_engine, exc, URL, text

CSV_FILE_PATH = path.join(path.dirname(__file__), "nimble_contacts_sheet.csv")

CURRENT_FILE_NAME = path.basename(__file__)

def connect():
    """
    Connects to a PostgreSQL database using the environment variables 
    "POSTGRES_DB", "POSTGRES_USER", and "POSTGRES_PASSWORD".

    :return: A connection object to the PostgreSQL database.
    """
    try:
        connction_url = URL.create(
            "postgresql+psycopg2",
            username=environ.get("POSTGRES_USER"),
            password=environ.get("POSTGRES_PASSWORD"),
            host="pdb",
            database=environ.get("POSTGRES_DB"),
            port=5432
        )
        engine = create_engine(connction_url)
        return engine
    # pylint: disable=broad-exception-caught
    except exc.OperationalError as err:
        print("OperationalError: ", err)
        return None


def check_seed_exists(engine):
    """
    Check if a seed exists in the database.

    Parameters:
        conn (connection): The database connection.

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
                    WHERE seed_name = :value1
                );
            """
            seed_exists = connection.execute(text(query), {'seed_name': CURRENT_FILE_NAME}).scalar()
            return seed_exists

def create_db_table(engine, query: str):
    """
    Creates a table in the PostgreSQL database with the name provided in query.
    """
    enable_uuid_ossp_query = text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    with engine.connect() as connection:
        connection.execute(enable_uuid_ossp_query)
        res = connection.execute(text(query))
        connection.commit()
        return res

def create_seeds_table(engine):
    """
    Creates a seeds table in the database if it does not already exist.

    Parameters:
        conn (Connection): The database connection object.

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

def create_user_table(engine):
    """
    Creates a table in the PostgreSQL database with the name "users".

    :param engine: A connection object to the PostgreSQL database.
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
        with open(CSV_FILE_PATH, newline='', encoding='utf-8', mode='r') as file:
            seed_data: dict = DictReader(file)
            result = []
            for row in seed_data:
                result.append({
                    "first_name": row.get('first name', "Was not provided"),
                    "last_name": row.get('last name', "Was not provided"),
                    "email": row.get('email', 'Was not provided'),
                    "description": row.get('description', 'Was not provided'),
                    })
            return result
    except OSError as err:
        print(err)
        return None

def seed_db(engine):
    """
    Seed the database with data from a CSV file.

    Parameters:
        engine (connection): The database connection.

    Returns:
        None
    """
    data = parse_csv()
    with engine.connect() as connection:
        seed_query: str = "INSERT INTO seeds (seed_name) VALUES (:seed_name);"
        user_query: str = """INSERT INTO users (
            first_name, last_name, email, description)
            VALUES (:first_name, :last_name, :email, :description);
        """
              
        connection.execute(text(user_query), data)
        connection.execute(text(seed_query), {
            'seed_name': CURRENT_FILE_NAME,
        })

        connection.commit()
        return "Done"
    return None





if __name__ == "__main__":
    db_engine = connect()
    if db_engine:
        print(db_engine)
        if check_seed_exists(db_engine):
            pass
        else:
            proc_pipe = [create_seeds_table, create_user_table]
            seed_result = list(map(lambda f: f(db_engine), proc_pipe))
            print("Creation of seeds table and user table:", seed_result)
            seed_db(db_engine)
