from django.shortcuts import render, get_object_or_404, redirect
from pipeline.models import Pipeline
from execution.models import PipelineRun
from execution.forms import PipelineRunForm  # we will create this
from django.contrib import messages

def catalogue(request):
    pipelines = Pipeline.objects.all()
    return render(request, "pipeline/catalogue.html", {"pipelines": pipelines})

def pipeline_detail(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id)

    if request.method == "POST":
        form = PipelineRunForm(request.POST, request.FILES)
        if form.is_valid():
            pipelineRun = form.save(commit=False)
            pipelineRun.pipeline = pipeline
            pipelineRun.save()
            # Trigger celery task here if needed
            from execution.tasks import run_pipeline
            run_pipeline.delay(pipelineRun.id)

            messages.success(request, "Pipeline submitted successfully!")
            return redirect("execution:home", run_id=pipelineRun.id)
    else:
        form = PipelineRunForm()

    return render(request, "pipeline/pipeline_details.html", {
        "pipeline": pipeline,
        "form": form
    })





