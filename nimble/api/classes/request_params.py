""" 
Nimb API Request Params
"""
from typing import List, Union, Optional, Literal, Tuple
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from utils.skip_none import dict_skip_none

AllowedFieldsType = List[Literal["first name", "last name", "email", "description"]]
SortField = Literal["updated"]
SortOrder = Literal["asc", "desc"]
SortFields = Tuple[Union[SortField], Union[SortOrder]]
RecordType = Literal["person"]


@dataclass
class RequestParams(DataClassJsonMixin):
    """
    Defines Nimb API request params
    """

    fields: AllowedFieldsType
    tags: int
    per_page: int
    sort: SortFields
    page: int = 1
    query: Optional[str] = None
    record_type: Optional[Union[RecordType]] = None

    def __post_init__(self):
        self.sort: str = ":".join(map(str, self.sort))
        self.fields: str = ",".join(map(str, self.fields))

    def to_dict_safe(self):
        """
        Converts the object to a dictionary, including all its attributes.

        :return: A dictionary representation of the object.
        :rtype: dict
        """
        default = self.__dict__
        return dict_skip_none(default)


request_params_schema = RequestParams.schema()
