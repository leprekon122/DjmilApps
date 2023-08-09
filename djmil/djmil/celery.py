
import os
from celery import Celery



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djmil.settings_files.settings")
app = Celery('djmil')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()