from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', broker=settings.CELERY_BROKER_URL)
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    timezone='Asia/Taipei',
    enable_utc=True,
    beat_schedule={
        # "name": {
        #     "task": "apps.app.tasks.run",
        #     "schedule": crontab(hour=1),  # 01:00 am running
        #     "args": ('',)
        # },
    }
)

# @celery.shared_task(default_retry_delay=60, ignore_result=True)
# def run():
#   pass
