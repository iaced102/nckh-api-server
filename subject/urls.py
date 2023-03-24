from django.urls import path, include
from .views import SubjectSearch,SubjectCreate,GetAllSubject

urlpatterns = [
    path('create/',SubjectCreate.as_view()),
    path('search/', SubjectSearch.as_view()),
    path('get-all/', GetAllSubject.as_view()),
    
]