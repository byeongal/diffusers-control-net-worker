from celery import Celery

import celery_config
from common.settings import celery_worker_settings


app = Celery(
    celery_worker_settings.worker_name,
    broker=f"{celery_worker_settings.broker_base_uri}/{celery_worker_settings.vhost_name}",
    include=["tasks"],
)
app.config_from_object(celery_config)
