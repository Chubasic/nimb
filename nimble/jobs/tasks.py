"""
Nimble domain tasks
"""
import datetime
from sqlalchemy import text
from datetime import datetime
from _celery import celery
from celery import chain
from ..api.classes.errors import ValidationError, QuotaError, NotFoundError, ServerError
from ..api.classes.request_params import RequestParams
from ..api.classes.response import response_fields_schema
from ..api.nimb import fetch
from db import engine as db_engine


@celery.task
def fetch_contacts():
    """
    Fetches contacts from the specified path using the given parameters.

    Returns:
        None: If an error occurs during the request.
    """
    path = "contacts"
    params = RequestParams(
        fields=["first name", "last name", "email", "description"],
        tags=0,
        per_page=20,
        page=1,
        sort=("updated", "desc"),
        record_type="person",
        query=None,
    )
    try:
        resposne = fetch(path, params=params)
        resources = resposne.get("resources")
        # Check how does it serialize that fast with recursion
        chain_res = chain(
            serialize_data.s(resources) | insert_data.s())

    except (ValidationError, QuotaError, NotFoundError, ServerError) as err:
        print("Task:: fetch_contacts::failed \n")
        print(err.message)
        raise err


@celery.task
def serialize_data(data):
    return response_fields_schema.load(data, many=True)



@celery.task
def insert_data(resp):
    print("Runin testing task", resp)
    user_query: str = """INSERT INTO users (
    first_name, last_name, email, description)
    VALUES (:first_name, :last_name, :email, :description);
    """
    with db_engine.connect() as conn:
        conn.execute(text(user_query), {
            'first_name': "Task_testing",
            'last_name': "Task_testing",
            'email': f"Task_testing {datetime.now()}",
            'description': "Task_testing"
        })
        conn.commit()
    return print("Testing task:: 'testing'")


@celery.task 
def error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
        request.id, exc, traceback))
    