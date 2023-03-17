from django.urls import path, include
from .views import SubjectSearch,SubjectCreate

urlpatterns = [
    path('create/',SubjectCreate.as_view()),
    path('search/', SubjectSearch.as_view()),
]