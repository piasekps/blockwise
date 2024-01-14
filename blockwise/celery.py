# celery.py
import os

from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blockwise.settings')

# create a Celery instance and configure it.
app = Celery('blockwise', broker='redis://redis:6379/0')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
