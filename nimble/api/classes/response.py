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
    Representation of Nimble API response resources[n].fields.
    Ingores undefined fields that are present in response body
    """

    fields: Contact


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ResponseContacts:
    """
    Serialize contact response
    Ingores undefined fields that are present in response body
    """

    resources: List[ResponseFields]


# pylint: disable=no-member
response_contacts_schema = ResponseContacts.schema()
response_fields_schema = ResponseFields.schema()
