from celery import Celery
from celery.schedules import crontab

from config import settings

celery = Celery(
    'celery',
    backend=settings.CELERY_BROKER_URL,
    broker=settings.CELERY_RESULT_BACKEND,
)

celery.autodiscover_tasks(['data'])

# TODO fix me
celery.conf.beat_schedule = {
    'every day at 1 PM': {
        'task': 'load_data',
        'schedule': crontab(minute='37', hour='12')
    },
}
