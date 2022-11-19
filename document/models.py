from django.db import models
from account.models import User
from subject.models import Subject
# Create your models here.


class Document(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='host')
    classId = models.CharField(max_length=25)
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='subject')


class SubTaskDocument(models.Model):
    field = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student')
    owner = models.ForeignKey(
        Document, related_name='owner', on_delete=models.CASCADE)
