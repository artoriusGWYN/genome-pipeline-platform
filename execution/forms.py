from django import forms
from .models import PipelineRun


class PipelineRunForm(forms.ModelForm):

    class Meta:
        model = PipelineRun
        fields = "__all__"
        exclude = ["pipeline", "status", "work_dir", "created_at"]