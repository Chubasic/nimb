from celery.schedules import crontab
from celery import Celery, signature
from os import environ

celery = Celery(
    f"nimble",
    broker=f"{environ.get('REDIS_CONNECTION_URL')}",
    backend=f"{environ.get('REDIS_CONNECTION_URL')}",
    include=['nimble.jobs.tasks']
)


def error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
        request.id, exc, traceback))


# celery.conf.update(app.config)
celery.conf.beat_schedule = {
    'add-every-minute': {
        'task': 'nimble.jobs.tasks.fetch_contacts',
        'schedule': crontab(minute='*/5'),
        'options': {
            # 'link': signature('nimble.jobs.tasks.testing_tasks', kwargs={'result': '{{ return }}'}),
            'link_error': signature('nimble.jobs.tasks.error_handler')
        }
    },
}
