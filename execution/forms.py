from django import forms
from .models import PipelineRun

class PipelineRunForm(forms.ModelForm):
    class Meta:
        model = PipelineRun
        fields = ["sequencing_type", "fastq_r1", "fastq_r2", "nanopore", "samplesheet", "parameters"]