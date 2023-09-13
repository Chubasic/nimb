"""
Nimble API response
"""
from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json, Undefined

from nimble.api.classes.contact import Contact


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ResponseFields:
    """
    Representation of Nimble API response.
    Ingores undefined fields that are present in response body
    """
    
    # This does not work :(
    fields: Contact


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ResponseResources:
    resources: List[ResponseFields]
