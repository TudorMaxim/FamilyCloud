from celery import Celery

from config import config

celery = Celery(__name__)


def setup_celery():
    celery.conf.update(
        broker=config.CELERY_BROKER_URL,
        backend=config.CELERY_RESULT_BACKEND,
        broker_connection_retry_on_startup=True,
    )
    celery.conf.imports = ("src.family_cloud_api.tasks",)  # Register celery tasks
