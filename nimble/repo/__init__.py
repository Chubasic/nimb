"""
Nimble repository
"""
from urllib.parse import unquote
from typing import Union, List, Tuple, Dict, Type
from sqlalchemy import Engine, text, CursorResult, Sequence, Row, inspect
from sqlalchemy.exc import SQLAlchemyError


# pylint: disable=fixme
# TODO: Abstract Repository class and implement it
class Repository:
    """
    Nimble repository.
    Performs operations on the database
    !NOT ALL FUNCTIONS ARE IMPLEMENTED!
    """

    db_engine: Engine
    table: str
    model_cls: Type
    _last_query: str

    def __init__(self, engine, table):
        self.db_engine = engine
        self.table = table

    def _exec(self, query, data) -> CursorResult | None:
        """
        Execute a database query and return the result.

        Args:
            query (str): The SQL query to execute.
            data (dict): The data to pass as parameters to the query.

        Returns:
            CursorResult | None: The result of the query if successful, None otherwise.
        """
        print("QUERY:", query)
        with self.db_engine.connect() as dbapi:
            with dbapi.begin():
                try:
                    result = dbapi.execute(text(query), data)
                    return result
                except SQLAlchemyError as db_err:
                    print("DB Error::", str(db_err))
                    return None

    @staticmethod
    def _populate_query(query: str, keys: List[str]) -> str:
        """
        Populates a given query string with the provided keys.

        Args:
            query (str): The query string to be populated.
            keys (List[str]): The list of keys to be used for populating the query string.

        Returns:
            str: The populated query string.
        """
        fields = ", ".join(keys)
        values = ", ".join(list(map(lambda val: ":" + val, keys)))
        return query.replace("$fields$", fields).replace("$values$", values)

    @staticmethod
    def _create_value_bindings(data: Union[Dict, List[Dict], Tuple[Dict]]):
        """
        Creates value bindings based on the given data.

        Parameters:
        - data: A Union of one dictionary, a list of dictionaries, or a tuple of dictionaries.
          The data from which to create value bindings.

        Returns:
        - If the data is a list of dictionaries, returns the keys of the first dictionary.
        - If the data is a single dictionary, returns the keys of the dictionary.
        - If the data is None, returns None.

        Raises:
        - TypeError: If the data is not a dictionary, a list of dictionaries,
        or a tuple of dictionaries.
        """
        match data:
            case [{**_keys}, *_rest]:
                return data[0].keys()
            case {**_keys}:
                return data.keys()
            case None:
                return None
            case _:
                raise TypeError(
                    f"Expected filled dict or list, but received {type(data).__name__}"
                )

    @staticmethod
    def _plain_to_tsquery(search: str) -> str:
        """
        Convert a plain search string to a tsquery format.

        Args:
            search (str): The plain search string to be converted.

        Returns:
            str: The tsquery format of the search string.
        """
        return unquote(search).replace(" ", " & ") + ":*"

    @staticmethod
    def _get_vectors(fields):
        """
        Generates a string by concatenating the values of the 'fields'
        dictionary and converting them to tsvector format.

        Parameters:
            fields (dict): A dictionary of field names and their corresponding values.

        Returns:
            str: A string representing the concatenated values of the 'fields'
            dictionary in tsvector format.
        """
        return "".join(
            list(
                map(
                    lambda idx_vec: (
                        # pylint: disable=consider-using-f-string
                        "{} {}".format(
                            f"to_tsvector(coalesce({idx_vec[1]}, ''))",
                            "" if idx_vec[0] + 1 == len(fields) else "|| ",
                        )
                    ),
                    enumerate(fields.values()),
                )
            )
        )

    def insert(self, data: Union[Dict, List[Dict], Tuple[Dict]]):
        """
        Inserts data into the table.

        Parameters:
            data (Union[Dict, List[Dict], Tuple[Dict]]):
            The data to be inserted into the table.

        Returns:
            Any: The result of the query execution.
        """

        query = f"""
        INSERT INTO {self.table} ($fields$)
        VALUES ($values$)
        ON CONFLICT DO NOTHING
        RETURNING id;"""

        keys = self._create_value_bindings(data)
        query = self._populate_query(query, keys)

        self._last_query = query
        return self._exec(query, data)

    def search(self, search: str, fields: Dict[str, str]):
        """
        Search for records in the table based on the given search term and field values.

        Args:
            search (str): The search term to be used for searching records.
            fields (Dict[str, str]): A dictionary of field names and their corresponding values.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the matched records.
        """

        prefixed_search = self._plain_to_tsquery(search)
        vectors = self._get_vectors(fields)
        query = f"SELECT * FROM {self.table} WHERE {vectors} @@ to_tsquery(:search);"

        result = self._exec(query, {"search": prefixed_search})
        if result:
            rows = result.all()
            return list(map(lambda r: r._asdict(), rows))
        else:
            return []

    def delete(self):
        """
        Deletes the object.

        Raises:
            NotImplementedError: This function is not implemented yet.
        """
        raise NotImplementedError
