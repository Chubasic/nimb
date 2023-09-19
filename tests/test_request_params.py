# pylint: skip-file
from typing import List, Union, Optional
import pytest
from nimble.api.classes.request_params import RequestParams


@pytest.fixture
def sample_params():
    return RequestParams(
        fields=["field1", "field2"],
        tags=5,
        per_page=10,
        sort=["field1", "asc"],
        page=1,
        query="example",
        record_type="type1",
    )


def test_sort_attribute(sample_params):
    # Check if the sort attribute is formatted correctly
    assert sample_params.sort == "field1:asc"


def test_fields_attribute(sample_params):
    # Check if the fields attribute is formatted correctly
    assert sample_params.fields == "field1,field2"


def test_to_dict_safe(sample_params):
    # Check if the to_dict_safe method returns the expected dictionary
    expected_dict = {
        "fields": "field1,field2",
        "tags": 5,
        "per_page": 10,
        "sort": "field1:asc",
        "page": 1,
        "query": "example",
        "record_type": "type1",
    }
    assert sample_params.to_dict_safe() == expected_dict
