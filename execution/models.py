# this models.py belong to the execution app 
from django.db import models
from pipeline.models import Pipeline


class PipelineRun(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("DONE", "Done"),
        ("FAILED", "Failed"),
    ]

    ASSEMBLER_CHOICES = [
        ("unicycler", "Unicycler"),
        ("canu", "Canu"),
        ("dragonflye", "Dragonflye"),
    ]

    ASSEMBLY_TYPE_CHOICES = [
        ("short", "Short reads"),
        ("long", "Long reads"),
        ("hybrid", "Hybrid"),
    ]

    ANNOTATION_CHOICES = [
        ("prokka", "Prokka"),
        ("bakta", "Bakta"),
        ("dfast", "DFAST"),
    ]

    BUSCO_LINEAGE_CHOICES = [
        ("bacteria_odb10", "Bacteria"),
        ("enterobacterales_odb10", "Enterobacterales"),
    ]

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)

    # INPUT FILES
    samplesheet = models.FileField(upload_to="samplesheets/", null=True, blank=True)
    fastq_r1 = models.FileField(upload_to="fastq/", null=True, blank=True)
    fastq_r2 = models.FileField(upload_to="fastq/", null=True, blank=True)
    nanopore = models.FileField(upload_to="fastq/", null=True, blank=True)

    email = models.EmailField(null=True, blank=True)

    # QC
    skip_fastqc = models.BooleanField(default=False)
    skip_fastp = models.BooleanField(default=False)
    skip_nanoplot = models.BooleanField(default=False)
    skip_toulligqc = models.BooleanField(default=False)
    save_trimmed = models.BooleanField(default=False)

    # Assembly
    assembler = models.CharField(
        max_length=50,
        choices=ASSEMBLER_CHOICES,
        default="unicycler"
    )

    assembly_type = models.CharField(
        max_length=50,
        choices=ASSEMBLY_TYPE_CHOICES,
        default="short"
    )

    # BUSCO
    busco_lineage = models.CharField(
        max_length=100,
        choices=BUSCO_LINEAGE_CHOICES,
        default="bacteria_odb10"
    )

    skip_busco = models.BooleanField(default=False)

    # Annotation
    annotation_tool = models.CharField(
        max_length=50,
        choices=ANNOTATION_CHOICES,
        default="prokka"
    )

    skip_annotation = models.BooleanField(default=False)

    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    work_dir = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run {self.id} - {self.status}"
