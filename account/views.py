from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, UserLoginSerializer
from document.views import User

from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class UserRegisterView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This user name has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                userName=serializer.validated_data['userName'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'message':'200_OK',
                    'status':status.HTTP_200_OK,
                    'userInfo': {
                        'userName': user.userName,
                        'userNameDisplay': user.userNameDisplay,
                        'orgChart': 'superUser' if user.is_superuser else('staff' if user.is_staff else 'user')
                    },
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'username or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfor(APIView):
    def get(self, request):
        return JsonResponse(status=status.HTTP_200_OK,)
        pass
        return JsonResponse({
            'error_messages': 'error',
            'view': {'request': request},
            'error_code': 200
        }, status=status.HTTP_200_OK)
#tự động tạo tài khoản cho sinh viên trong ds mk gửi lên nếu chưa có (username = msv , usernamedis = userndis)
#istaff = false , 
# class creatAccount(APIView):
#     def post(self,request):
#         if not User.objects.filter(userName=id).exists():
#             user = User.objects.create_user(id, password='1')
#             user.save()
