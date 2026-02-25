from django.urls import path
from . import views

app_name = "execution"

urlpatterns = [
    path("<int:run_id>/", views.pipeline_detail, name="home")  # run detail page
]