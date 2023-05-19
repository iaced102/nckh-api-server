from django.shortcuts import render
from rest_framework.views import APIView
from .models import Subject
from .serializers import SubjectSerializer,SubjectCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.http import JsonResponse
import json


class SubjectCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if not request.user.is_superuser:
            return Response({
                "status": 401,
                "message": "you are not super user, don't have permission"
            }, status=status.HTTP_401_UNAUTHORIZED)
        subject = Subject.objects.filter(subjectId = request.data["subjectId"])
        serializer = SubjectCreateSerializer(data=request.data)
        if serializer.is_valid() and len(subject)==0:
            serializer.save()
            return Response({
                "status": 200,
                "message": "create successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({"message":"this subject exist", status:400}, status=status.HTTP_400_BAD_REQUEST)

        
class SubjectSearch(APIView):
    def get(self,request):
        keyword = request.query_params.get('keyword')
        if keyword:
           queryset = Subject.objects.filter(name__contains=keyword)
           queryset |= Subject.objects.filter(description__contains=keyword)
           queryset |= Subject.objects.filter(customField__contains=keyword)
           queryset |= Subject.objects.filter(subjectId__contains=keyword)
        else:
           queryset = Subject.objects.all()
        serializer = SubjectSerializer(queryset, many=True)
        result = []
        for data in serializer.data:
           result.append(data)
        return Response(result)

class GetAllSubject(APIView):
    def get(self, request):
        subject = Subject.objects.all()
        # data = SubjectSerializer(subject, many = True).data
        
        # print(data)
        return JsonResponse({
                "status": 200,
                "data": list(subject.values())
            }, status=status.HTTP_200_OK)