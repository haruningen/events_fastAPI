from celery import Celery
from celery.schedules import crontab

from config import settings

celery = Celery(
    'celery',
    backend=settings.CELERY_BROKER_URL,
    broker=settings.CELERY_RESULT_BACKEND,
)

celery.autodiscover_tasks(['data'])

celery.conf.beat_schedule = {
    'every day at 3 PM': {
        'task': 'load_data_task',
        'schedule': crontab(minute='00', hour='15')
    },
}
