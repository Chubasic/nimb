"""
Nimble contact repository
"""
from typing import Union, Dict, List, Tuple
from db.query_builder import QueryBuilder
from db.classes.repository import Repository
from db import engine as db_engine


class ContactRepo(Repository):
    """
    Contact aka users repository, CRUD operations are (should be) implemented here
    Performs operations on the database
    !NOT ALL METHODS ARE IMPLEMENTED!
    """

    def __init__(self):
        self.query_builder = QueryBuilder(db_engine, "users")

    def insert(self, data: Union[Dict, List[Dict], Tuple[Dict]]):
        return self.query_builder.insert(data)

    def search(self, search: str, fields: List[str]):
        return self.query_builder.search(search, fields, to_dict=True)
