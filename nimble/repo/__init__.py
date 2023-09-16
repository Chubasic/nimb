"""
Nimble repository
"""
from sqlalchemy import Engine


class NimbleRepository:
    db_engine: Engine
    
    def __init__(self, engine):
        self.db_engine = engine
        
    def insert(self):
        raise NotImplementedError
    
    def create(self):
        raise NotImplementedError
    
    def delete(self):
        raise NotImplementedError
    
    def search(self, search_str):
        raise NotImplementedError
