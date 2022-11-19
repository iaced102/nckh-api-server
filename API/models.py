from django.db import models
from rest_framework.authentication import SessionAuthentication

# Create your models here.


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass
