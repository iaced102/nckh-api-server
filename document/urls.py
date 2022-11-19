from django.urls import path
from django.urls import path, include
from .views import createDocument
urlpatterns = [
    path('create', createDocument.as_view())
]
