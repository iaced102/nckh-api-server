from django.db import models
import jsonfield
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    customField = jsonfield.JSONField()
