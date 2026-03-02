from django.urls import path
from . import views

# urls.py that belongs to the execution app

app_name = "execution"

urlpatterns = [
    path("run/<int:run_id>/", views.run_detail, name="run_detail"),
    path("run/<int:run_id>/download/<path:filepath>", views.download_file, name="download_file"),
    path("comparison/", views.comparison, name="comparison"),
]






