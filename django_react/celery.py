from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab


# default Django settings for the celery program, also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_react.settings")

# base redis url set as default redis'
BASE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

app = Celery("django_react", include=["django_react.tasks"])

# string here means the worker need not serialize the configuration object
# to child processes
app.config_from_object("django.conf:settings", namespace="CELERY")
# namespace will propagate as a prefix to all celery-based configuration keys

# load task modules from all registered Django app configs
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# enables scheduling items in the Django admin
app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"

app.conf.beat_schedule = {
    "add-every-minute-crontab": {
        "task": "django_react.tasks.xsum",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
        "args": (16, 16),
    },
    "add-every-5-seconds": {
        "task": "django_react.tasks.mul",
        "schedule": 5.0,
        "args": (16, 16),
    },
    "add-every-30-seconds": {
        "task": "django_react.tasks.add",
        "schedule": 30.0,
        "args": (16, 16),
    },
}
