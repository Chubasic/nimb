"""
Nimble API response
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined

from nimble.api.classes.contact import Contact


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ResponseFields:
    """
    Representation of Nimble API response.
    Ingores undefined fields that are present in response body
    """
    fields: Contact


response_fields_schema = ResponseFields.schema()
