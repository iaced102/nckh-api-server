from rest_framework import serializers
from .models import Document, SubTaskDocument


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['host', 'classId', 'id','columnDefs']


class SubTaskDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTaskDocument
        fields = ['student', 'owner','value']
