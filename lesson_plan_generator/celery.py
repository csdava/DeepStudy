# DjangoProject3/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject3.settings')
app = Celery('DjangoProject3')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()