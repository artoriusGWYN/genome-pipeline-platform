from django.urls import path
from . import views

app_name = "execution"

urlpatterns = [
    path("run/<int:run_id>/", views.run_detail, name="run_detail"),
]