from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import DocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from document.models import Document,SubTaskDocument
from rest_framework import permissions


from rest_framework.views import APIView
# Create your views here.
from rest_framework.authentication import SessionAuthentication


# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         pass


class createDocument(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # get user by userName = request.user
        user = User.objects.get(userName=request.user)
        document =Document.objects.create(host=user,classId=request.data["classId"])
        document.save()
        for col in request.data['columnDefs']:
            field = col["field"]
            headerName= col["headerName"]

            if field != 'userNameDisplay':
                for data in request.data["rawData"]:
                    student = data["userNameDisplay"]
                    value = data[field]
                    print(value)    
                    subtask = SubTaskDocument.objects.create(field = field,title = headerName,student = student,owner = document,value = value)
                    subtask.save()
        list = SubTaskDocument.objects.all()
        print(list)
        return Response('asdjf;l')
        #tự động tạo tài khoản cho sinh viên trong ds mk gửi lên nếu chưa có (uername = msv , userndis = userndis)
        #istaff = fall , 
    # def get_object(self):
    #     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)
    #     return obj
# class SubscriberViewSet(ModelViewSet):
#     serializer_class = SubscriberSerializer
#     queryset = Subscriber.objects.all()
#     permission_classes = (IsAuthenticated,)
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user