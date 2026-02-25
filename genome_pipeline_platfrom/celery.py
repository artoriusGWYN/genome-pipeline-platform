import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "genome_pipeline_platfrom.settings")
app = Celery("genome_pipeline_platfrom")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()