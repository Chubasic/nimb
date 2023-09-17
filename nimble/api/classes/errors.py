from typing import Optional
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class NimbleError(Exception):
    """
    Basic Nimble erorr
    """

    code = 0
    message: str
    nimble_code: int = field(metadata=config(field_name="code"))


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ValidationError(NimbleError):
    """
    Sent on invalid parameters.
    Returns with HTTP code 409 and code field equal to 245.
    """

    code = 245
    error_messages: Optional[dict] = field(metadata=config(field_name="errors"))


class QuotaError(NimbleError):
    """
    Sent if user exceeded his quota values.
    Returns with HTTP code 402 and code field equal to 108.
    """

    code = 108


class ServerError(NimbleError):
    """
    Sent if unrecoverable Nimble server occurs.
    Returns with HTTP code 500 and code field equal to 107.
    """

    code = 107


class Unauthorized(NimbleError):
    """
    Sent if Authorization token is invalid
    """

    code = 403


@dataclass
class NotFoundError(Exception, DataClassJsonMixin):
    """
    Sent on attempt to get some object by invalid identifier
    (in most cases identifier of object is its ID in our database).
    """

    object_type: str
    object_id: str


class Unsupported(Exception, DataClassJsonMixin):
    """
    This exception is raised when an unsupported response error occurs.

    Attributes:
        message (str): The error message describing the unsupported response error.
    """

    message: "Unsupported response error"
