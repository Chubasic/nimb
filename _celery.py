""" 
Define the Celery app with configuration, and register the scheduled (beat) tasks
"""
from os import environ
from celery.schedules import crontab
from celery import Celery, signature

celery = Celery(
    "nimble",
    broker=f"{environ.get('REDIS_CONNECTION_URL')}",
    backend=f"{environ.get('REDIS_CONNECTION_URL')}",
    include=["nimble.jobs.tasks"],
)


celery.conf.beat_schedule = {
    "add-every-minute": {
        "task": "nimble.jobs.tasks.fetch_contacts",
        "schedule": crontab(minute="* * * * *"),
        "options": {"link_error": signature("nimble.jobs.tasks.error_handler")},
    },
}
