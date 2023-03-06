from django.urls import path, include
from .views import SubjectSearch

urlpatterns = [
    path('search/', SubjectSearch.as_view()),
]