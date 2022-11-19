from rest_framework import serializers
from .models import Document, SubTaskDocument


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['host', 'classId', 'subject']


class SubTaskDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTaskDocument
        fields = ['field', 'title', 'student', 'owner']
