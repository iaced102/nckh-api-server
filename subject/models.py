from django.db import models
import jsonfield
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    customField = jsonfield.JSONField(),
<<<<<<< HEAD
    subjectId = models.CharField(max_length=20, default="")
=======
    subjectId = models.CharField(max_length=20, default='')
>>>>>>> aa7857daf33ca167a2c2ae472e8a88d74321f433
