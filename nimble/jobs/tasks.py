"""
Nimble domain tasks
"""
import datetime

from sqlalchemy import text
from datetime import datetime
from _celery import celery
from ..api.classes.errors import ValidationError, QuotaError, NotFoundError, ServerError
from ..api.classes.request_params import RequestParams
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
        per_page=100,
        page=1,
        sort=('updated', 'desc'),
        record_type="person",
        query="",
    )
    try:
        print("Task:: fetch_contacts::running \n")
        resposne = fetch(path, params=params)
        chain = testing_tasks.s(resposne)
        chain.apply_async()
    except (ValidationError, QuotaError, NotFoundError, ServerError) as err:
        print("Task:: fetch_contacts::failed \n")
        print(err.message)
        raise err


@celery.task
def testing_tasks(resp):
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
    