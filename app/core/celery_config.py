from celery import Celery
from app.core.settings import redis_settings
# Initialize Celery
celery_app = Celery(
    'celery',
    broker=redis_settings.__str__(),
    backend=redis_settings.__str__(),
)
