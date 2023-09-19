"""
Nimble domain tasks
"""
import datetime
from dataclasses import asdict

from sqlalchemy import text
from datetime import datetime
from _celery import celery
from celery import chain
from ..api.classes.request_params import RequestParams, SortOrder, SortField
from ..api.classes.response import ResponseContacts
from ..api.nimb import fetch
from db import engine as db_engine
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
def format_data(data):
    print("Flattening data::", data)
    flatten = list(map(lambda r: {**r.get('fields', {})}, data.get('resources')))
    return flatten


@celery.task
def insert_data(flatten):
    print("Inserting...")
    Repository(db_engine).insert(flatten)
    return print("Testing task:: 'fetch_contacts.insert_data'")


@celery.task 
def error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
        request.id, exc, traceback))
    