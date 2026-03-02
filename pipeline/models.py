from django.db import models



class Pipeline(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name