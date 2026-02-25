from django.shortcuts import render, get_object_or_404, redirect
from pipeline.models import Pipeline
from execution.models import PipelineRun
from execution.forms import PipelineRunForm
from execution.tasks import run_pipeline

def pipeline_detail(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id)

    if request.method == "POST":
        form = PipelineRunForm(request.POST, request.FILES)
        if form.is_valid():
            run = form.save(commit=False)
            run.pipeline = pipeline
            run.save()

            # Launch Celery task
            run_pipeline.delay(run.id)

            return redirect("execution:home")  # or any success page
    else:
        form = PipelineRunForm()

    return render(request, "pipeline/pipeline_details.html", {"pipeline": pipeline, "form": form})
