from django.urls import path
from . import views

#urls.py that belongs to the pipeline app

app_name = "pipeline"

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("<int:pipeline_id>/", views.pipeline_detail, name="pipeline_detail"),
]