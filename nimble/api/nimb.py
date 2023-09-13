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
    Unsupported, NimbleError
)
from .classes.request_params import RequestParams

BASE_URL = environ.get("NIMBLE_API_URI")
TOKEN_PREFIX = "Bearer"
DEFAULT_HEADERS = {
    "Authorization": TOKEN_PREFIX + " " + environ.get("NIMBLE_AUTH_TOKEN")
}


def fetch(endpoint: str, params: RequestParams):
    print(endpoint, params)
    """
    Get data from Nimb API
    """
    print(BASE_URL)
    if BASE_URL:
        try:
            url = urljoin(BASE_URL, endpoint)
            print(url)
            response = requests.get(
                url,
                params=parse.urlencode(params.to_dict_safe(), safe=':,'),
                headers={
                    **DEFAULT_HEADERS
                },
                timeout=10,
            )
            print("Request path", response.request.url)
            if response.status_code == 200:
                return response.json()

            response.raise_for_status()
        except requests.exceptions.RequestException as req_err:
            print(f"Unable fetch data from Nimb API, on route {endpoint}")
            if isinstance(req_err, Timeout):
                print(req_err)
                return NimbleError.schema().load({
                    'message': 'Service is unavaliable',
                    'code': 0
                })
            print("Status code", req_err.response.status_code)
            error_body = req_err.response.json()
            match req_err.response.status_code:
                case 404:
                    return NotFoundError.schema().load(error_body)
                case 403 | 401:
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

            
