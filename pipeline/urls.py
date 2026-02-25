from django.urls import path
from . import views

app_name = "pipeline"

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("<int:pipeline_id>/", views.pipeline_detail, name="pipeline_detail"),
]