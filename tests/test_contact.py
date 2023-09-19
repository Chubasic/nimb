"""
Contact dataclass tests
"""
# pylint: skip-file
import pytest
from nimble.api.classes.contact import Contact


@pytest.fixture
def contact_with_data():
    return Contact(
        first_name=[{"value": "John"}],
        last_name=[{"value": "Doe"}],
        email=[{"value": "john.doe@example.com"}],
        description=[{"value": "Test description"}],
    )


@pytest.fixture
def contact_without_data():
    return Contact()


def test_first_name(contact_with_data, contact_without_data):
    print(contact_with_data)
    assert contact_with_data.first_name == "John"
    assert contact_without_data.first_name == "No data"


def test_last_name(contact_with_data, contact_without_data):
    assert contact_with_data.last_name == "Doe"
    assert contact_without_data.last_name == "No data"


def test_email(contact_with_data, contact_without_data):
    assert contact_with_data.email == "john.doe@example.com"
    assert contact_without_data.email == "No data"


def test_description(contact_with_data, contact_without_data):
    assert contact_with_data.description == "Test description"
    assert contact_without_data.description == "No description"
