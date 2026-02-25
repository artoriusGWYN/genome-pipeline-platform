from django.db import models

# Create your models here.


class Pipeline(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    accepts_file = models.BooleanField(default=True)

    def __str__(self):
        return self.name




#class bacass(models.Model):
#    inputFile = models.FileField(upload_to="bacass_input/")
#    read_types = models.CharField(max_length=20)
#
#class pangenome(models.Model):
#    inputFile = models.FileField(upload_to="pangenome_input")
#    haploTypeNumber = models.IntegerField()
#
#class mag(models.Model):
#    inputFile = models.FileField(upload_to="mag_input")
#    status = models.CharField(max_length=20, default="PENDING")
#
#
#
#    
#class JOB(models.Model):
#    PIPELINES = [("nf-core/Bacass", "Bacass"),
#                ("nf-core/pangenome", "Pangenome"),
#                ("nf-core/mag", "mag")]
#    
#    inputFile = models.FileField(upload_to="inputs/")
#    inputType = models.CharField(max_length=50)
#    inputPipeline = models.CharField(max_length=100, choices=PIPELINES)
#    status = models.CharField(max_length=20, default="PENDING")
#    inputPath = models.TextField()
#    outputPath = models.TextField()
#    time_creation = models.DateTimeField(auto_now_add=True)
