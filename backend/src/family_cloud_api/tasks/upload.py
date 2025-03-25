import time

from src.family_cloud_api.celery import celery


@celery.task(name="upload")
def upload():
    time.sleep(5)
    return "TODO: implement upload task"
