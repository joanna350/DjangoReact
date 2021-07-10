# Django starts so that shared_task uses the app
from .celery import app as celeryApp
