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
from .serializers import SubjectSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

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
        return Response(serializer.data)
# em quên mất cách viết đoạn này r : 
#   lặp qua serializer đó rồi append vào result rồi response cái result đấy về

