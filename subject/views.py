from django.shortcuts import render

# Create your views here.
# 1 tạo API tạo subject,
# 2 API tìm kiếm subject
#     - nhận vào 1 keyword,
#     - Subject.object.filter(id__contains=request.data.key)
#     - Subject.object.filter(name__...)
#     - quăng cả 2 cái trên vào serializer.dât
#     - lặp qua serializer đó rồi append vào result rồi response cái result đấy về
from rest_framework.views import APIView
from .models import Subject
from .serializers import SubjectSerializer,SubjectCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


class SubjectCreate(APIView):
    def post(self, request):
        serializer = SubjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


