from django.shortcuts import render, get_object_or_404
from .models import PipelineRun

def run_detail(request, run_id):
    run = get_object_or_404(PipelineRun, id=run_id)
    return render(request, "execution/run_detail.html", {"run": run})
