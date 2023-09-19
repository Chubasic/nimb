"""
Nimble repository
"""
from typing import Union, List, Tuple, Dict
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError


def populate_query(query: str,  keys: List[str]) -> str:
    fields = ', '.join(keys)
    values = ', '.join(
        list(map(lambda val: ":"+val, keys))
    )
    return query.replace('$fields$', fields).replace("$values$", values)


class Repository:
    db_engine: Engine
    _last_query: str
    
    def __init__(self, engine):
        self.db_engine = engine
        
    def _exec(self, query, data):
        with self.db_engine.connect() as db:
            with db.begin():
                try:
                    db.execute(text(query), data)
                    # print("res.returns_rows?", res.returns_rows) // False
                    # print("res.returned_defaults_rows?", res.returned_defaults_rows) // None
                    return 1
                except SQLAlchemyError as db_err:
                    print(db_err.__str__())
                    return 0
    
    @staticmethod
    def _keys_from_args(data: Union[Dict, List[Dict], Tuple[Dict]]) -> Union[List[str] | None]:
        match data:
            case [{**_keys}, *_rest]:
                return data[0].keys()
            case {**_keys}:
                return data.keys()
            case None:
                return None
            case _:
                raise TypeError(f"Expected filled dict or list, but received {type(data).__name__}")

    def insert(self, data: Union[Dict, List[Dict], Tuple[Dict]]):
        query = """
        INSERT INTO users ($fields$)
        VALUES ($values$)
        ON CONFLICT DO NOTHING
        RETURNING users.id;"""

        keys = self._keys_from_args(data)

        query = populate_query(query, keys)
        self._last_query = query
        return self._exec(query, data)

    def delete(self):
        raise NotImplementedError
    
    def search(self, search: str, fields: List[str]):
    # pseudo!
    #      vectors = ""
    #     for (const [i, vec] of fields.values())
            # vectors = vectors.concat(`to_tsvector(coalesce(${vec}, '')) ${i + 1 == fields.__len__ ? "" : " or "}`);
    #
        #     return query.raw(`((${vectors}) @@ plainto_tsquery(?))`, search + ":*");
    #

        raise NotImplementedError
