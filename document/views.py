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

from rest_framework.views import APIView
# Create your views here.
from rest_framework.authentication import SessionAuthentication


# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         pass


class createDocument(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        return Response('asdjf;l')
