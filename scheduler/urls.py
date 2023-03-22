from django.urls import path
from django.urls import path, include

from .views import createScheduler,ViewSessions

urlpatterns = [
    path('create', createScheduler.as_view(), name='scheduler-create'),
    path('sessions', ViewSessions.as_view(), name='view-sessions'),
]