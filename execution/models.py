from django.db import models

class PipelineRun(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("DONE", "Done"),
        ("FAILED", "Failed"),
    ]

    pipeline = models.ForeignKey("pipeline.Pipeline", on_delete=models.CASCADE)

    sequencing_type = models.CharField(
        choices=[
            ("PE", "Paired-end"),
            ("LR", "Long-read"),
            ("HY", "Hybrid"),
        ],
        max_length=2,
        default="PE"
    )

    # Files uploaded by user
    fastq_r1 = models.FileField(blank=True, null=True)
    fastq_r2 = models.FileField(blank=True, null=True)
    nanopore = models.FileField(blank=True, null=True)

    # Ready-made TSV (samplesheet)
    samplesheet = models.FileField(upload_to="samplesheets/", blank=True, null=True)

    parameters = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    work_dir = models.TextField(null=True, blank=True)
    result_dir = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"PipelineRun {self.id} - {self.pipeline.name}"
