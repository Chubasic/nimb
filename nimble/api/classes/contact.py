"""
Describes Contact aka user in Nimble API response and locally in DB 
"""
from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import (
    DataClassJsonMixin, config, dataclass_json, Undefined, LetterCase,
)


@dataclass
class Contact(DataClassJsonMixin):
    first_name: List[dict] = field(
        metadata=config(field_name="first name"))

    last_name: List[dict] = field(
        metadata=config(field_name="last name"))

    email: Optional[List[dict]] = None
    description: Optional[List[dict]] = None
    
    def __post_init__(self):
        self.first_name: str = \
            self.first_name[0].get("value") if self.first_name else "No data"

        self.last_name: str = \
            self.last_name[0].get("value") if self.last_name else "No data"
        
        self.description: Optional[str] = \
            self.description[0].get("value") if self.description else "No description"

        self.email: Optional[str] = \
            self.email[0].get("value") if self.email else "No data"


contact_schema = Contact.schema()
