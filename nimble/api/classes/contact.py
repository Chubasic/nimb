"""
Describes Contact aka user in Nimble API response and locally in DB 
"""
from dataclasses import dataclass, field
from typing import List
from dataclasses_json import (
    DataClassJsonMixin,
    Undefined,
    LetterCase,
    dataclass_json, config,
)


@dataclass
# @dataclass_json(undefined=Undefined.EXCLUDE, letter_case=LetterCase.SNAKE)
class Contact(DataClassJsonMixin):
    first_name: List[dict] = field(metadata=config(field_name="first name"))
    last_name: List[dict] = field(metadata=config(field_name="last name"))
    email: List[dict]
    description: List[dict]
    
    def __post_init__(self):
        self.first_name: str = self.first_name[0].get("value", "No data")
        self.last_name: str = self.last_name[0].get("value", "No data")
        self.description: str = self.description[0].get("value", "No description")
        self.email: str = self.email[0].get("value", "No data")
        