"""
Repository class
"""
from abc import ABC, abstractmethod
from typing import Union, List, Tuple, Dict
from db.query_builder import QueryBuilder


class Repository(ABC):
    """
    Repository abs class, defines what kind of methods should.

    !NOT ALL FUNCTIONS ARE IMPLEMENTED!
    """

    query_builder: QueryBuilder

    @abstractmethod
    def insert(self, data: Union[Dict, List[Dict], Tuple[Dict]]):
        """Perfrom insertion of data into the table"""
        raise NotImplementedError

    @abstractmethod
    def search(self, search: str, fields: List[str]):
        """Perform search"""
