from django.db import models

# Create your models here.
class pipeline(models.Model):
    pipelineId = models.IntegerField()
    piplineName = models.CharField(max_length=30)

