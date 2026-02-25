from django.urls import path
from . import views


app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("pipeline_guidance/", views.guidance, name="guidance"),

]