# execution/tasks.py
from celery import shared_task
from .models import PipelineRun
import time

@shared_task
def run_pipeline(run_id):
    run = PipelineRun.objects.get(id=run_id)
    
    run.status = "running"
    run.save()

    time.sleep(5)  

    run.status = "completed"
    run.save()
    return f"PipelineRun {run_id} completed"