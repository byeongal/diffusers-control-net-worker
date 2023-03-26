# Celery configuration
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
from kombu import Queue


# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_acks_late
task_acks_late = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-worker_prefetch_multiplier
worker_prefetch_multiplier = 1
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_queues
task_queues = [Queue(name="diffusers-control-net")]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_ignore_result
task_ignore_result = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-broker_connection_timeout
broker_connection_timeout = 360
