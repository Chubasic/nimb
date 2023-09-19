""" 
Nimble API ruqests
"""
from urllib.parse import urljoin
from os import environ
import requests
from urllib import parse

from requests import Timeout

from .classes.errors import (
    NotFoundError,
    ValidationError,
    QuotaError,
    ServerError,
    Unauthorized,
    Unsupported,
    NimbleError,
)
from .classes.request_params import RequestParams
from .classes.response import response_contacts_schema

BASE_URL = environ.get("NIMBLE_API_URI")
TOKEN_PREFIX = "Bearer"
DEFAULT_HEADERS = {
    "Authorization": TOKEN_PREFIX + " " + environ.get("NIMBLE_AUTH_TOKEN")
}


def fetch(endpoint: str, params: RequestParams):
    """
    Get data from Nimb API
    """
    if BASE_URL:
        try:
            url = urljoin(BASE_URL, endpoint)
            print(url)
            response = requests.get(
                url,
                params=parse.urlencode(params.to_dict_safe(), safe=":,"),
                headers={**DEFAULT_HEADERS},
                timeout=10,
            )
            response.raise_for_status()

            if response.status_code == 200:
                # Check how does it serialize that fast with recursion
                return response_contacts_schema.load(response.json())

        except requests.exceptions.RequestException as req_err:
            print(f"Unable fetch data from Nimb API, on route {endpoint}")
            if isinstance(req_err, Timeout):
                return NimbleError.schema().load(
                    {"message": "Service is unavaliable", "code": 0}
                )
            error_body = req_err.response.json()
            match req_err.response.status_code:
                case 404:
                    return NotFoundError.schema().load(error_body)
                case 403 | 401:
                    # pylint: disable=no-member
                    return Unauthorized.schema().load(error_body)

            match error_body.get("code"):
                case ValidationError.code:
                    return ValidationError.schema().load(error_body)

                case QuotaError.code:
                    return QuotaError.schema().load(error_body)

                case ServerError.code:
                    return ServerError.schema().load(error_body)

                case _:
                    print("Unsupported")
                    return Unsupported()
