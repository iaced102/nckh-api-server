from django.db import models
from account.models import User
from subject.models import Subject
# Create your models here.


class Document(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='host')
    classId = models.CharField(max_length=25)
    sharePermission = models.CharField(max_length=15,default = "onlyMe")
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name='subject', null=True)


class SubTaskDocument(models.Model):
    field = models.CharField(max_length=20)
    # field
    # title tuong ung voi headerName
    title = models.CharField(max_length=50)
    # userName Display
    # student = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='student')
    student = models.CharField(max_length=100,default="")
    # thuoc ve docuemnt nao
    owner = models.ForeignKey(
        Document, related_name='owner', on_delete=models.CASCADE)
    value = models.CharField(max_length=50,default="")

