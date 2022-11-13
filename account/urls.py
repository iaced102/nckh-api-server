from django.urls import path
from rest_framework_simplejwt import views as jwt_views
# from car.views import UserRegisterView
from .views import UserRegisterView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'),
]
