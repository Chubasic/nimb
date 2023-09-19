"""
Nimble module tasks.
Logs avaliable on debug mode
"""
from typing import Dict
from dataclasses import asdict
from celery import chain
from _celery import celery
from db import engine as db_engine
from ..api.classes.request_params import RequestParams, SortOrder, SortField
from ..api.classes.response import ResponseContacts
from ..api.nimb import fetch
from ..repo import Repository


@celery.task
def fetch_contacts():
    """
    Fetches contacts from the specified path using the given parameters.

    Returns:
        None: If an error occurs during the request.
    """
    path = "contacts"
    sort_field: SortField = "updated"
    order: SortOrder = "desc"
    params = RequestParams(
        fields=["first name", "last name", "email", "description"],
        tags=0,
        per_page=20,
        page=1,
        sort=(sort_field, order),
        record_type="person",
        query=None,
    )
    response = fetch(path, params=params)
    match response:
        case ResponseContacts():
            chain(format_data.s(asdict(response)), insert_data.s()).apply_async()
        case _:
            print("Task::fetch_contacts::failed \n")
            raise response


@celery.task
def format_data(data: Dict):
    """
    Format the given data by flattening it.

    Args:
        data (Dict): The data to be formatted.

    Returns:
        List[Dict]: The flattened data.
    """
    print("Flattening data::", data)
    flatten = list(map(lambda r: {**r.get("fields", {})}, data.get("resources")))
    return flatten


@celery.task
def insert_data(flatten):
    """
    Inserts the given data into the "users" collection in the database.

    Args:
        flatten (bool): Whether to flatten the data before inserting it.
    """
    print("Inserting...")
    Repository(db_engine, "users").insert(flatten)
    return print("Testing task:: 'fetch_contacts.insert_data'")


@celery.task
def error_handler(request, exc, traceback):
    """
    A Celery task function that handles errors raised during task execution.

    Args:
        request: The request object associated with the task.
        exc: The exception that was raised during task execution.
        traceback: The traceback information for the exception.
    """
    # pylint: disable=consider-using-f-string
    print("Task {0} raised exception: {1!r}\n{2!r}".format(request.id, exc, traceback))
