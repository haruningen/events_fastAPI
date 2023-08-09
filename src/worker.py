from celery import Celery

from config import settings

celery = Celery('celery',
                backend=settings.CELERY_BROKER_URL,
                broker=settings.CELERY_RESULT_BACKEND)
# celery.autodiscover_tasks(['data'])
# celery.conf.beat_schedule = {
#     'run-me-every-ten-seconds': {
#         'task': 'load_data',
#         'schedule': 10.0
#     }
# }
