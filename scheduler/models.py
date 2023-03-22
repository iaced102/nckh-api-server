from django.db import models
from account.models import User
from document.models import Document,SubTaskDocument
# Create your models here.

class Classroom(models.Model):
    room_id = models.CharField(max_length=10,unique=True)
class Scheduler(models.Model):
    classroom = models.ForeignKey(Classroom,related_name="scheduler", on_delete=models.CASCADE)
    document = models.ForeignKey(Document,related_name="scheduler", on_delete=models.CASCADE)
class Sessions(models.Model):
    # session = models.CharField(max_length=2,default='')
    classroom = models.ForeignKey(Classroom,related_name="sessions", on_delete=models.CASCADE)
    scheduler = models.ForeignKey(Scheduler,related_name="sessions", on_delete=models.CASCADE)
    user_applied = models.TextField()
    date = models.DateField()
    time_slot = models.IntegerField()

