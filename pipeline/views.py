from django.shortcuts import render, get_object_or_404, redirect
from .models import Pipeline
from execution.forms import PipelineRunForm
from execution.tasks import run_pipeline



def catalogue(request):
    pipelines = Pipeline.objects.all()
    return render(request, "pipeline/catalogue.html", {
        "pipelines": pipelines
    })


def pipeline_detail(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id)

    if request.method == "POST":
        form = PipelineRunForm(request.POST, request.FILES)

        if form.is_valid():
            run = form.save(commit=False)
            run.pipeline = pipeline
            run.status = "PENDING"
            run.save()

            run_pipeline.delay(run.id)

            return redirect("execution:run_detail", run_id=run.id)

    else:
        form = PipelineRunForm()

    return render(request, "pipeline/pipeline_details.html", {
        "pipeline": pipeline,
        "form": form
    })


